from .base import BaseHandler
from .base import BaseRefreshHandler
from ..utility import error_print


SERVER_TYPE_PATTERN = r"^\{[a-z]+\}server$"


class InstallRefreshHandler(BaseRefreshHandler):
    def fore_children(self, phase, settings, variables):
        super().fore_children(phase, settings, variables)

        if self._resource.state == 0:
            server_resource = self._resource.get_ancestor(SERVER_TYPE_PATTERN)
            ssh_client = server_resource._ssh_client
            package = self._resource.properties['package']
            command = 'pip2 --disable-pip-version-check install "{0}"'.format(package)
            exit_status, stdout, stderr = ssh_client.execute(command, False)

            if exit_status == 0:
                text = '\033[32;1m{0}\033[0m = \033[30;1m{1}\033[0m\n'.format(exit_status, command)
            else:
                text = '\033[31;1m{0}\033[0m = \033[30;1m{1}\033[0m\n'.format(exit_status, command)

                if stderr:
                    text += '\033[31;1m{0}\033[0m\n'.format(stderr)

                if stdout:
                    text += '\033[32;1m{0}\033[0m\n'.format(stdout)

            self._out.write(text)


class InstallHandler(BaseHandler):
    def __init__(self, resource):
        super().__init__(InstallRefreshHandler, None, resource)

    def validate(self):
        if not 'package' in self._resource.properties:
            error_print(
                '{0}:{1} "pip2:install" element requires "package" attribute.',
                self._resource.source_file,
                self._resource.source_line)


class UninstallRefreshHandler(BaseRefreshHandler):
    def fore_children(self, phase, settings, variables):
        super().fore_children(phase, settings, variables)

        if self._resource.state == 0:
            server_resource = self._resource.get_ancestor(SERVER_TYPE_PATTERN)
            ssh_client = server_resource._ssh_client
            package = self._resource.properties['package']
            command = 'pip2 --disable-pip-version-check -uninstall "{0}"'.format(package)
            exit_status, stdout, stderr = ssh_client.execute(command)

            if exit_status == 0:
                text = '\033[32;1m{0}\033[0m = \033[30;1m{1}\033[0m\n'.format(exit_status, command)
            else:
                text = '\033[31;1m{0}\033[0m = \033[30;1m{1}\033[0m\n'.format(exit_status, command)

                if stderr:
                    text += '\033[31;1m{0}\033[0m\n'.format(stderr)

                if stdout:
                    text += '\033[32;1m{0}\033[0m\n'.format(stdout)

            self._out.write(text)


class UninstallHandler(BaseHandler):
    def __init__(self, resource):
        super().__init__(UninstallRefreshHandler, None, resource)

    def validate(self):
        if not 'package' in self._resource.properties:
            error_print(
                '{0}:{1} "pip2:uninstall" element requires "package" attribute.',
                self._resource.source_file,
                self._resource.source_line)
