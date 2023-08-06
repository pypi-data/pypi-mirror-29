import logging
import textwrap
import time

from xblock.core import XBlock
from xblock.fields import Scope, Float, String, Dict, List
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader
from xblockutils.studio_editable import StudioEditableXBlockMixin
from xblockutils.settings import XBlockWithSettingsMixin

from .utils import UP_STATES, SETTINGS_KEY, DEFAULT_SETTINGS
from .utils import get_xblock_configuration
from .tasks import LaunchStackTask, SuspendStackTask, CheckStudentProgressTask

logger = logging.getLogger(__name__)
loader = ResourceLoader(__name__)


@XBlock.wants('settings')
class HastexoXBlock(XBlock,
                    XBlockWithSettingsMixin,
                    StudioEditableXBlockMixin):
    """
    Provides lab environments and an SSH connection to them.

    """
    # Settings with defaults.
    display_name = String(
        default="Lab",
        scope=Scope.settings,
        help="Title to display")
    weight = Float(
        default=1,
        scope=Scope.settings,
        help="Defines the maximum total grade of the block.")

    # Mandatory: must be set per instance.
    stack_template_path = String(
        scope=Scope.settings,
        help="The relative path to the uploaded orchestration template. "
             "For example, \"hot_lab.yaml\".")
    stack_user_name = String(
        scope=Scope.settings,
        help="The name of the training user in the stack.")
    stack_protocol = String(
        values=["ssh", "rdp", "vnc"],
        default="ssh",
        scope=Scope.settings,
        help="What protocol to use for the connection. "
             "Currently, \"ssh\", \"rdp\", or \"vnc\".")
    stack_ports = List(
        default=[],
        scope=Scope.settings,
        help="What ports are available in the stack.")
    stack_port_names = List(
        default=[],
        scope=Scope.settings,
        help="Names of ports defined above.")
    provider = String(
        default="default",
        scope=Scope.settings,
        help="Where to launch the stack.")

    # Set exclusively via XML
    tests = List(
        default=[],
        scope=Scope.content,
        help="The list of tests to run.")

    # User state, per instance.
    stack_run = String(
        default="",
        scope=Scope.user_state,
        help="The name of the run")
    stack_name = String(
        default="",
        scope=Scope.user_state,
        help="The name of the user's stack")
    check_id = String(
        default="",
        scope=Scope.user_state,
        help="The check task id")
    check_status = Dict(
        default=None,
        scope=Scope.user_state,
        help="The check status")

    # Stack states per user, across all courses
    stacks = Dict(
        default={},
        scope=Scope.preferences,
        help="Stack states for this user's courses: one entry per stack")

    editable_fields = (
        'display_name',
        'weight',
        'stack_template_path',
        'stack_user_name',
        'stack_protocol',
        'stack_ports',
        'stack_port_names',
        'provider')

    has_author_view = True
    has_score = True
    has_children = True
    icon_class = 'problem'
    block_settings_key = SETTINGS_KEY

    @classmethod
    def parse_xml(cls, node, runtime, keys, id_generator):
        block = runtime.construct_xblock_from_class(cls, keys)

        # Find <test> children
        for child in node:
            if child.tag == "test":
                text = child.text

                # Fix up whitespace.
                if text[0] == "\n":
                    text = text[1:]
                text.rstrip()
                text = textwrap.dedent(text)

                block.tests.append(text)
            else:
                block.runtime.add_node_as_child(block, child, id_generator)

        # Attributes become fields.
        for name, value in node.items():
            if name in block.fields:
                value = (block.fields[name]).from_string(value)
                setattr(block, name, value)

        return block

    def author_view(self, context=None):
        """ Studio View """
        msg = u"This XBlock only renders content when viewed via the LMS."
        return Fragment(u'<em>%s</em></p>' % msg)

    def is_correct(self):
        if not (self.check_status and isinstance(self.check_status, dict)):
            return False
        else:
            total = self.check_status.get('total')
            if not total:
                return False
            else:
                score = self.check_status.get('pass')
                return score == total

    def get_block_ids(self):
        course_id = self.xmodule_runtime.course_id
        anonymous_student_id = self.xmodule_runtime.anonymous_student_id

        return (course_id, anonymous_student_id)

    def get_stack_template(self):
        """
        Load the stack template directly from the course's content store.

        Note: accessing the contentstore directly is not supported by the
        XBlock API, so this depends on keeping pace with changes to
        edx-platform itself.  Because of it, this should be replaced with an
        HTTP GET to the LMS, in the future.

        """
        course_id, _ = self.get_block_ids()
        stack_template = None
        try:
            from xmodule.contentstore.content import StaticContent
            from xmodule.contentstore.django import contentstore
            from xmodule.exceptions import NotFoundError

            loc = StaticContent.compute_location(course_id,
                                                 self.stack_template_path)
            asset = contentstore().find(loc)
            stack_template = asset.data
        except (ImportError, NotFoundError):
            pass

        return stack_template

    def student_view(self, context=None):
        """
        The primary view of the HastexoXBlock, shown to students when viewing
        courses.
        """
        def error_frag(msg):
            """ Build a fragment to display runtime errors. """
            context = {'error_msg': msg}
            html = loader.render_template('static/html/error.html', context)
            frag = Fragment(html)
            frag.add_css_url(
                self.runtime.local_resource_url(self,
                                                'public/css/main.css')
            )
            return frag

        # Load configuration
        configuration = self.get_configuration()

        # Get the course id and anonymous user id, and derive the stack name
        # from them
        course_id, anonymous_student_id = self.get_block_ids()
        self.stack_run = "%s_%s" % (course_id.course, course_id.run)
        self.stack_name = "%s_%s" % (self.stack_run, anonymous_student_id)

        # Render the HTML template
        html = loader.render_template('static/html/main.html')
        frag = Fragment(html)

        # Add the public CSS and JS
        frag.add_css_url(
            self.runtime.local_resource_url(self, 'public/css/main.css')
        )
        frag.add_javascript_url(
            self.runtime.local_resource_url(self, 'public/js/plugins.js')
        )
        frag.add_javascript_url(
            self.runtime.local_resource_url(self, 'public/js/main.js')
        )

        # Set the port
        port = None
        if len(self.stack_ports) > 0:
            port = self.stack_get("port")
            if not port or port not in self.stack_ports:
                port = self.stack_ports[0]
                self.stack_set("port", port)

        # Call the JS initialization function
        frag.initialize_js('HastexoXBlock', {
            "terminal_url": configuration.get("terminal_url"),
            "timeouts": configuration.get("js_timeouts"),
            "has_tests": len(self.tests) > 0,
            "protocol": self.stack_protocol,
            "ports": self.stack_ports,
            "port_names": self.stack_port_names,
            "port": port,
            "provider": self.provider
        })

        return frag

    def get_configuration(self):
        """
        Get the configuration data for the student_view.

        """
        settings = self.get_xblock_settings(default=DEFAULT_SETTINGS)
        return get_xblock_configuration(settings, self.provider)

    def stack_set(self, prop, value):
        if not self.stacks.get(self.stack_name):
            self.stacks[self.stack_name] = {}

        self.stacks[self.stack_name][prop] = value

    def stack_get(self, l1=None, l2=None):
        retval = self.stacks.get(self.stack_name)
        if retval and l1:
            retval = retval.get(l1)
            if retval and l2:
                retval = retval.get(l2)

        return retval

    def suspend_user_stack(self, configuration):
        suspend_timeout = configuration.get("suspend_timeout")
        if suspend_timeout:
            # If the suspend task is pending, revoke it.
            stack_suspend_id = self.stack_get("suspend_id")
            if stack_suspend_id:
                logger.info(
                    'Revoking suspend task [%s] for [%s]' % (stack_suspend_id,
                                                             self.stack_name)
                )
                from lms import CELERY_APP
                CELERY_APP.control.revoke(stack_suspend_id)
                self.stack_set("suspend_id", None)

            # (Re)schedule the suspension in the future.
            args = (configuration, self.stack_name)
            task = SuspendStackTask()
            result = task.apply_async(args=args, countdown=suspend_timeout)
            logger.info(
                'Scheduled suspend task [%s] '
                'for [%s] in %s seconds' % (result.id,
                                            self.stack_name,
                                            suspend_timeout)
            )
            self.stack_set("suspend_id", result.id)
            self.stack_set("suspend_timestamp", int(time.time()))

    def launch_stack_task(self, args):
        configuration = args[0]
        task = LaunchStackTask()
        result = task.apply_async(
            args=args,
            expires=configuration.get('launch_timeout')
        )
        logger.info(
            'Launch task id for '
            'stack [%s] is: [%s]' % (self.stack_name, result.id)
        )

        return result

    def launch_stack_task_result(self, task_id):
        return LaunchStackTask().AsyncResult(task_id)

    @XBlock.json_handler
    def get_user_stack_status(self, data, suffix=''):
        configuration = self.get_configuration()

        def _launch_stack(reset=False):
            args = (
                configuration,
                self.stack_run,
                self.stack_name,
                self.get_stack_template(),
                self.stack_user_name,
                reset
            )

            logger.info('Firing async launch '
                        'task for [%s]' % (self.stack_name))
            result = self.launch_stack_task(args)

            # Save task ID and timestamp
            self.stack_set("launch_id", result.id)
            self.stack_set("launch_timestamp", int(time.time()))

            return result

        def _process_result(result):
            if result.ready():
                if (result.successful() and
                        isinstance(result.result, dict) and not
                        result.result.get('error')):
                    status = result.result
                else:
                    status = {
                        "status": "ERROR",
                        "error_msg": "Unexpected result: %s" % repr(result.result)  # noqa: E501
                    }
            else:
                status = {"status": "PENDING"}

            # Save status
            self.stack_set("status", status)

            return status

        def _process_error(error_msg):
            status = {
                "status": "ERROR",
                "error_msg": error_msg
            }

            # Save status
            self.stack_set("status", status)

            return status

        # Calculate the time since the suspend timer was last reset.
        now = int(time.time())
        suspend_timeout = configuration.get("suspend_timeout")
        suspend_timestamp = self.stack_get("suspend_timestamp")
        time_since_suspend = 0
        if suspend_timeout and suspend_timestamp:
            time_since_suspend = now - suspend_timestamp

        # Request type
        initialize = data.get("initialize", False)
        reset = data.get("reset", False)

        # Get the last stack status
        last_status_string = ""
        last_status = self.stack_get("status")
        if last_status:
            last_status_string = last_status.get("status", "")

        # No last stack status: this is the first time
        # the user launches this stack.
        if not last_status_string:
            logger.info('Launching stack [%s] '
                        'for the first time.' % (self.stack_name))
            result = _launch_stack(reset)
            status = _process_result(result)

        # There was a previous attempt at launching the stack
        elif last_status_string == "PENDING":
            # Update task result
            result = self.launch_stack_task_result(self.stack_get("launch_id"))
            status = _process_result(result)

            current_status_string = status.get('status')

            # Stack is still PENDING since last check.
            if current_status_string == "PENDING":
                # Calculate time since launch
                launch_timestamp = self.stack_get("launch_timestamp")
                time_since_launch = now - launch_timestamp
                launch_timeout = configuration.get('launch_timeout')

                # Check if the pending task hasn't timed out.
                if time_since_launch <= launch_timeout:
                    # The pending task still has some time to finish.
                    # Please wait.
                    logger.info('Launch pending for [%s]' % (self.stack_name))

                elif initialize or reset:
                    # Timeout reached, but the user just entered the page or
                    # requested a reset.  Try launching the stack again.
                    if initialize:
                        logger.info('Launch timeout detected on initialize. '
                                    'Launching stack [%s]' % (self.stack_name))
                    else:
                        logger.info('Launch timeout detected on reset. '
                                    'Resetting stack [%s]' % (self.stack_name))
                    result = _launch_stack(reset)
                    status = _process_result(result)

                else:
                    # Timeout reached.  Consider the task a failure and let the
                    # user retry manually.
                    logger.error('Launch timeout reached for [%s] '
                                 'after %s seconds' % (self.stack_name,
                                                       time_since_launch))
                    status = _process_error("Timeout when launching "
                                            "or resuming stack.")

            # Stack changed from PENDING to COMPLETE.
            elif current_status_string in UP_STATES:
                if reset or (suspend_timeout and time_since_suspend >= suspend_timeout):  # noqa: E501
                    if reset:
                        logger.info('Resetting successfully launched '
                                    'stack [%s].' % (self.stack_name))
                    else:
                        logger.info('Stack [%s] may have suspended. '
                                    'Relaunching.' % (self.stack_name))
                    result = _launch_stack(reset)
                    status = _process_result(result)

                # The stack couldn't have been suspended, yet.
                else:
                    logger.info('Successful launch detected for [%s], '
                                'with status [%s]' % (self.stack_name,
                                                      current_status_string))

            # Detected a failed launch attempt, but the user has requested a
            # retry, just entered the page, or requested a reset, so start from
            # scratch.
            elif initialize or reset:
                if reset:
                    logger.info('Resetting failed '
                                'stack [%s].' % (self.stack_name))
                else:
                    logger.info('Retrying previously failed '
                                'stack [%s].' % (self.stack_name))
                result = _launch_stack(reset)
                status = _process_result(result)

            # Detected a failed launch attempt.
            # Report the error and let the user retry manually.
            else:
                logger.error('Failed launch detected for [%s], '
                             'with status [%s]' % (self.stack_name,
                                                   current_status_string))

        # The stack was previously launched successfully
        elif last_status_string in UP_STATES:
            if reset or (suspend_timeout and time_since_suspend >= suspend_timeout):  # noqa: E501
                if reset:
                    logger.info('Resetting successfully launched '
                                'stack [%s].' % (self.stack_name))
                else:
                    logger.info('Stack [%s] may have suspended. '
                                'Relaunching.' % (self.stack_name))
                result = _launch_stack(reset)
                status = _process_result(result)

            else:
                logger.info('Successful launch detected for [%s], '
                            'with status [%s]' % (self.stack_name,
                                                  last_status_string))
                status = last_status

        # Detected a failed launch attempt, but the user just entered the page,
        # or requested a retry or reset, so start from scratch.
        elif initialize or reset:
            if reset:
                logger.info('Resetting failed stack [%s].' % (self.stack_name))
            else:
                logger.info('Retrying previously failed '
                            'stack [%s].' % (self.stack_name))
            result = _launch_stack(reset)
            status = _process_result(result)

        # Detected a failed launch attempt.  Report the error and let the user
        # retry manually.
        else:
            logger.error('Failed launch detected for [%s], '
                         'with status [%s]' % (self.stack_name,
                                               last_status_string))
            status = last_status

        # Restart the dead man's switch, if necessary.
        self.suspend_user_stack(configuration)

        return status

    @XBlock.json_handler
    def keepalive(self, data, suffix=''):
        configuration = self.get_configuration()

        # Restart the dead man's switch, if necessary.
        self.suspend_user_stack(configuration)

    @XBlock.json_handler
    def get_check_status(self, data, suffix=''):
        """
        Checks the current student score.
        """
        configuration = self.get_configuration()

        def _launch_check():
            stack_ip = self.stack_get("status", "ip")
            stack_key = self.stack_get("status", "key")
            logger.info('Executing tests for stack [%s], IP [%s], user [%s]:' %
                        (self.stack_name, stack_ip,
                         self.stack_user_name))
            for test in self.tests:
                logger.info('Test: %s' % test)

            args = (
                configuration,
                self.tests,
                stack_ip,
                self.stack_user_name,
                stack_key
            )
            result = CheckStudentProgressTask().apply_async(args=args,
                                                            expires=60)

            # Save task ID
            self.check_id = result.id

            return result

        def _process_result(result):
            if result.ready():
                # Clear the task ID so we know there is no task running.
                self.check_id = ""

                if (result.successful() and
                        isinstance(result.result, dict) and not
                        result.result.get('error')):
                    status = result.result

                    # Publish the grade
                    self.runtime.publish(self, 'grade', {
                        'value': status['pass'],
                        'max_value': status['total']
                    })
                else:
                    status = {
                        'status': 'ERROR',
                        'error_msg': 'Unexpected result: %s' % repr(result.result)  # noqa: E501
                    }
            else:
                status = {'status': 'PENDING'}

            # Store the result
            self.check_status = status

            return status

        # If a check task is running, return its status.
        if self.check_id:
            logger.info('Check progress task is running: %s' % self.check_id)
            result = CheckStudentProgressTask().AsyncResult(self.check_id)
            status = _process_result(result)

        # Otherwise, launch the check task.
        else:
            result = _launch_check()
            status = _process_result(result)

        return status

    @XBlock.json_handler
    def set_port(self, data, suffix=''):
        # Set the preferred stack port
        self.stack_set("port", int(data.get("port")))

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("HastexoXBlock",
             """<vertical_demo>
                <hastexo/>
                </vertical_demo>
             """),
        ]
