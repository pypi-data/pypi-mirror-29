import argparse
import logging

# to provide gettext for the overwritten methods from NonExitParser, because the native argparse does so.
try:
    from gettext import gettext as _
except ImportError:
    def _(message):
        return message

# local
try:
    from ts3ekkoclient.errors import EkkoParsingError, EkkoArgparserMessage
except ImportError:
    from .errors import EkkoParsingError, EkkoArgparserMessage

class NonExitParser(argparse.ArgumentParser):
    def exit(self, status=0, message=None):
        if message:
            raise EkkoParsingError(message, self.format_usage())

    def error(self, message):
        args = {'prog': self.prog, 'message': message}
        self.exit(2, _('%(prog)s: error: %(message)s\n') % args)

    def print_help(self, file=None):
        """
        Catch the help generation and raise the flowcontrol EkkoArgparserMessage instead.
        """
        raise EkkoArgparserMessage(self.format_help())

    def print_usage(self, file=None):
        """
        Catch the usage generation and raise the flowcontrol EkkoArgparserMessage instead.
        """
        raise EkkoArgparserMessage(self.format_usage())

class PermissionParser:
    @staticmethod
    def parse_add(cmd_prefix, cmd_str, **kwargs):
        """
        :param cmd_prefix: prefix, which should be removed from the cmd_str before processing (e.g. "!permission add")
        :param cmd_str: complete command string (e.g. "!permission add -c 12 -s 1 -s 9 control.spawn")
        :return: (permission_name, unique_id, channel_group, server_groups)
        """
        parser = NonExitParser(prog=cmd_prefix, **kwargs)
        parser.add_argument('permission_name')
        parser.add_argument('-d', '--deny', action='store_true')
        parser.add_argument('-i', '--unique-id')
        parser.add_argument('-c', '--channel-group')
        parser.add_argument('-s', '--server-group', action='append')
        args = parser.parse_args(cmd_str[len(cmd_prefix):].split())
        return args.permission_name, args.unique_id, args.channel_group, args.server_group, args.deny

    @staticmethod
    def parse_get(cmd_prefix, cmd_str, **kwargs):
        """
        :param cmd_prefix: prefix, which should be removed from the cmd_str before processing (e.g. "!permission get")
        :param cmd_str: complete command string (e.g. "!permission get control.spawn")
        :return: permission_name
        """
        parser = NonExitParser(prog=cmd_prefix, **kwargs)
        parser.add_argument('permission_name')
        args = parser.parse_args(cmd_str[len(cmd_prefix):].split())
        logging.debug(args)
        return args.permission_name

    @staticmethod
    def parse_delete(cmd_prefix, cmd_str, **kwargs):
        """
        :param cmd_prefix: prefix, which should be removed from the cmd_str before processing (e.g. "!permission get")
        :param cmd_str: complete command string (e.g. "!permission get control.spawn")
        :return: grant_id
        """
        parser = NonExitParser(prog=cmd_prefix, **kwargs)
        parser.add_argument('grant_id', type=int)
        args = parser.parse_args(cmd_str[len(cmd_prefix):].split())
        logging.debug(args)
        return args.grant_id

    @staticmethod
    def parse_info(cmd_prefix, cmd_str, **kwargs):
        return PermissionParser.parse_get(cmd_prefix, cmd_str, **kwargs)


class TextAliasParser:
    @staticmethod
    def parse_get(cmd_prefix, cmd_str, **kwargs):
        parser = NonExitParser(prog=cmd_prefix, **kwargs)
        parser.add_argument('-p', '--permanent', action='store_true')
        parser.add_argument('aliasname')
        args = parser.parse_args(cmd_str[len(cmd_prefix):].split())
        return args.permanent, args.aliasname

    @staticmethod
    def parse_delete(cmd_prefix, cmd_str, **kwargs):
        return TextAliasParser.parse_get(cmd_prefix, cmd_str, **kwargs)

    @staticmethod
    def parse_set(cmd_prefix, cmd_str, **kwargs):
        parser = NonExitParser(prog=cmd_prefix, **kwargs)
        parser.add_argument('-p', '--permanent', action='store_true')
        parser.add_argument('aliasname')
        parser.add_argument('value', nargs='*')
        args = parser.parse_args(cmd_str[len(cmd_prefix):].split())
        return args.permanent, args.aliasname, ' '.join(args.value or [])


class MediaAliasParser:
    @staticmethod
    def parse_queue(cmd_prefix, cmd_str, **kwargs):
        parser = NonExitParser(prog=cmd_prefix, **kwargs)
        parser.add_argument('--position', '-p', type=int)
        parser.add_argument('uri', nargs='+')
        args = parser.parse_args(cmd_str[len(cmd_prefix):].split())
        return args.position, args.uri

    @staticmethod
    def parse_skip(cmd_prefix, cmd_str, **kwargs):
        parser = NonExitParser(prog=cmd_prefix, **kwargs)
        parser.add_argument('count', default=1, nargs='?', type=int)
        args = parser.parse_args(cmd_str[len(cmd_prefix):].split())
        return args.count

    @staticmethod
    def parse_volume(cmd_prefix, cmd_str, **kwargs):
        parser = NonExitParser(prog=cmd_prefix, **kwargs)
        parser.add_argument('percentage', type=int)
        args = parser.parse_args(cmd_str[len(cmd_prefix):].split())
        return args.percentage

    @staticmethod
    def parse_media(cmd_prefix, cmd_str, **kwargs):
        parser = NonExitParser(prog=cmd_prefix, **kwargs)
        parser.add_argument('query_type', nargs='?', type=str)
        args = parser.parse_args(cmd_str[len(cmd_prefix):].split())
        return args.query_type or None

    @staticmethod
    def parse_mediaalias_get(cmd_prefix, cmd_str, **kwargs):
        parser = NonExitParser(prog=cmd_prefix, **kwargs)
        parser.add_argument('aliasname')
        args = parser.parse_args(cmd_str[len(cmd_prefix):].split())
        return args.aliasname

    @staticmethod
    def parse_mediaalias_set(cmd_prefix, cmd_str, **kwargs):
        parser = NonExitParser(prog=cmd_prefix, **kwargs)
        parser.add_argument('aliasname')
        parser.add_argument('value', nargs='+')
        args = parser.parse_args(cmd_str[len(cmd_prefix):].split())
        return args.aliasname, ' '.join(args.value or [])

    @staticmethod
    def parse_mediaalias_append(cmd_prefix, cmd_str, **kwargs):
        parser = NonExitParser(prog=cmd_prefix, **kwargs)
        parser.add_argument('aliasname')
        parser.add_argument('appendage', nargs='+')
        args = parser.parse_args(cmd_str[len(cmd_prefix):].split())
        return args.aliasname, ' '.join(args.appendage)

    @staticmethod
    def parse_mediaalias_delete(cmd_prefix, cmd_str, **kwargs):
        parser = NonExitParser(prog=cmd_prefix, **kwargs)
        parser.add_argument('aliasname')
        args = parser.parse_args(cmd_str[len(cmd_prefix):].split())
        return args.aliasname

class UtilityParser:
    @staticmethod
    def parse_name(cmd_prefix, cmd_str, **kwargs):
        parser = NonExitParser(prog=cmd_prefix, **kwargs)
        parser.add_argument('name', nargs='+')
        args = parser.parse_args(cmd_str[len(cmd_prefix):].split())
        return ' '.join(args.name)

    @staticmethod
    def parse_noargs(cmd_prefix, cmd_str, **kwargs):
        parser = NonExitParser(prog=cmd_prefix, **kwargs)
        args = parser.parse_args(cmd_str[len(cmd_prefix):].split())
        return args