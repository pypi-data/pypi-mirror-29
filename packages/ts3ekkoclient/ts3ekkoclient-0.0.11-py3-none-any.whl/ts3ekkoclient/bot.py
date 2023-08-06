import logging
import requests
import ts3.response
from ts3ekkoutil.envconsts import EkkoPropertyNames as epn

try:
    from ts3ekkoclient.ts3ekko import TS3Ekko
    from ts3ekkoclient.cogs.media import MediaCog
    from ts3ekkoclient.cogs.text import TextCog
    from ts3ekkoclient.event_type import EventType
    from ts3ekkoclient.errors import EkkoUnsuitedCommand, EkkoParsingError, EkkoNonexistentPermissionDoc, \
        EkkoArgparserMessage, EkkoNonexistentGrant
    from ts3ekkoclient.models import Invoker, startup
    from ts3ekkoclient.permission import PermissionManager, InvokerCtx
    from ts3ekkoclient.argparser import PermissionParser, UtilityParser
except ImportError:
    from .ts3ekko import TS3Ekko
    from .cogs.media import MediaCog
    from .cogs.text import TextCog
    from .event_type import EventType
    from .errors import EkkoUnsuitedCommand, EkkoParsingError, EkkoNonexistentPermissionDoc, EkkoArgparserMessage, \
        EkkoNonexistentGrant
    from .models import Invoker, startup
    from .permission import PermissionManager, InvokerCtx
    from .argparser import PermissionParser, UtilityParser

logger = logging.getLogger('ekkoclient-ekkobot')


class EkkoCorePermission:
    SPAWN = 'control.spawn'
    DESPAWN = 'control.despawn'
    JOIN = 'control.join'
    NAME = 'control.name'

    WHOAMI = 'other.whoami'

    PERMISSION_ADD = 'permission.add'
    PERMISSION_DELETE = 'permission.delete'
    PERMISSION_GET = 'permission.get'
    PERMISSION_INFO = 'permission.info'


class EkkoBot(TS3Ekko):
    def __init__(self, args):
        self.args = args
        super().__init__(apikey=args[epn.TS3_CLIENT_APIKEY], server=args[epn.TS3_CLIENTQUERY_HOST],
                         port=args[epn.TS3_CLIENTQUERY_PORT], bot_username=args[epn.TS3_USERNAME])

        self.register_hooks()
        self.dbsession = startup(self.args[epn.DB_USERNAME], self.args[epn.DB_PASSWORD], self.args[epn.DB_HOST],
                                 self.args[epn.DB_DBNAME])
        self.permission_manager = PermissionManager(self, self.dbsession)

        self.add_cog(MediaCog(self, self.args, self.dbsession))
        self.add_cog(TextCog(self, self.args, self.dbsession))

    def can(self, permission: str, event: ts3.response.TS3Event, quiet=False,
            deny_msg='Sorry, can\'t do that. You might not have the required permission for that.',
            quiet_permission_name=False, invoker_ctx: InvokerCtx = None) -> bool:
        """
        Can/Permission-Check relay with invoker specification to permission manager

        :param permission: name of the required permission
        :param event: TS3Event from which the required invoker information can be read from
        :param quiet: if True, the method wont reply to the event with a "denied" message in case of denied permission
        :param deny_msg: content of message that should be sent out when the action/permission was denied
        :param quiet_permission_name: if True, the method wont mention the required permission in case of denied permission
        :param invoker_ctx: if specified, use the specified invoker context instead of determining it from the passed event
        :return: bool, if the invoker is allowed to perform the action or not
        """
        if invoker_ctx is None:
            invoker_ctx = self.parse_invoker_context(event[0])
        if not self.permission_manager.can(permission, invoker_ctx):
            if not quiet and quiet_permission_name:
                self.reply(deny_msg, event)
            elif not quiet and not quiet_permission_name:
                self.reply(f'{deny_msg} (permission name: {permission})', event)
            return False
        else:
            return True

    def parse(self, parse_func, event: ts3.response.TS3Event, *args, **kwargs):
        """
        Calls a parsing function with the given arguments. Replies with usage and error in teamspeak to the event,
        should the parsing be not successful.

        :param parse_func: a argparser function (see in `~ts3ekkoclient.parser`)
        :param event: a ts3 event to which can be replied
        :param args: args for the parser function
        :param kwargs: kwargs for the parser function
        :returns: from the parse_func
        :raises EkkoParsingError: if parse_func is not successful
        :raises EkkoArgparserMessage: if user requested help/usage information
        """
        try:
            return parse_func(*args, **kwargs)
        except EkkoParsingError as e:
            # Something was missing (required args e.g.)
            self.reply(e.__str__(), event)
            raise
        except EkkoArgparserMessage as e:
            # These are messages like help or usage
            self.reply(e.__str__(), event)
            # This exception should be excepted further up the handling chain and be quietly discarded,
            # while also aborting the handling (because it was handled succesfully).
            raise

    def register_hooks(self):
        """
        Enables command hooks for events like spawning and despawning.
        FIXME: would really like this to be decorators, guess I could do that sometimes in the future
        """
        self.add_command(EventType.TEXTMESSAGE, self.relay_spawn, help_cmd_str='!spawn')
        self.add_command(EventType.TEXTMESSAGE, self.relay_despawn, help_cmd_str='!despawn')
        self.add_command(EventType.TEXTMESSAGE, self.cmd_join, help_cmd_str='!join')
        self.add_command(EventType.TEXTMESSAGE, self.cmd_help)
        self.add_command(EventType.TEXTMESSAGE, self.cmd_name, help_cmd_str='!name')
        self.add_command(EventType.TEXTMESSAGE, self.cmd_whoami, help_cmd_str='!whoami')
        self.add_command(EventType.TEXTMESSAGE, self.cmd_permission, priority=75, help_cmd_str='!permission')
        self.add_command(EventType.TEXTMESSAGE, self.cmd_permission_add, help_cmd_str='!permission')
        self.add_command(EventType.TEXTMESSAGE, self.cmd_permission_get, help_cmd_str='!permission')
        self.add_command(EventType.TEXTMESSAGE, self.cmd_permission_info, help_cmd_str='!permission')
        self.add_command(EventType.TEXTMESSAGE, self.cmd_permission_delete, help_cmd_str='!permission')
        self.add_command(EventType.CONNECTSTATUSCHANGE, self.init_description)

    def relay_spawn(self, event):
        """
        Command: !spawn

        Relays the spawn command to the management instance which in turn spawns a new bot instance which connects 
        to the channel the invoker of the command is in.

        :param event: TS3Event
        """
        if self.check_cmd_suitability('^!spawn', event[0]['msg']):
            if self.can(EkkoCorePermission.SPAWN, event):
                invoker_clid = event[0]['invokerid']
                invoker_cid = self.ts3conn.cid_from_clid(invoker_clid)
                requests.get(f'http://{self.args[epn.EKKO_MANAGE_SERVER]}:{self.args[epn.EKKO_MANAGE_PORT]}'
                             f'/cmd/spawn/{invoker_cid}')

    def relay_despawn(self, event):
        """
        Command: !despawn

        Kills the bot instance this was messaged to. Relays the message to the management instance for cleanups.

        :param event: TS3Event
        """
        if self.check_cmd_suitability('^!despawn', event[0]['msg']):
            if self.can(EkkoCorePermission.DESPAWN, event):
                self.reply('Exiting now! o/', event)
                requests.get(f'http://{self.args[epn.EKKO_MANAGE_SERVER]}:{self.args[epn.EKKO_MANAGE_PORT]}'
                             f'/cmd/despawn/{self.args[epn.EKKO_NODE_ID]}')
                exit(0)

    def init_description(self, event):
        """
        Not yet implemented due to design fault/bug in the ClientQuery API.
        => changing own description requires dbproperties-edit permission, which you usually dont have.
        
        See: https://forum.teamspeak.com/threads/134743-ClientQuery-edit-own-description
        """
        if event[0]['status'] == 'connection_established':
            pass
        raise EkkoUnsuitedCommand()

    def cmd_join(self, event):
        """
        Command: !join

        Moves the bot instance into the channel the invoker of the command is in. 
        
        # TODO: add support for channel passwords

        :param event: TS3Event
        """
        cmd_prefix = '!join'
        if self.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            if self.can(EkkoCorePermission.JOIN, event):
                self.parse(UtilityParser.parse_noargs, event, cmd_prefix, event[0]['msg'],
                           description='Make this bot instance join your channel.')
                invoker_clid = event[0]['invokerid']
                invoker_cid = self.ts3conn.cid_from_clid(invoker_clid)
                bot_clid = self.ts3conn.whoami()[0]['clid']
                self.ts3conn.clientmove(clid=bot_clid, cid=invoker_cid)

    def cmd_name(self, event):
        """
        Command: !name

        Renames this bot instance to the given name.
        
        See `UtilityParser.parse_name` for parameters.

        :param event: TS3Event
        """
        cmd_prefix = '!name'
        if self.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            if self.can(EkkoCorePermission.NAME, event):
                name = self.parse(UtilityParser.parse_name, event, '!name', event[0]['msg'],
                                  description='Change the bot\'s username')
                self.ts3conn.clientupdate(client_nickname=name)

    def cmd_whoami(self, event):
        """
        Command: !whoami

        Replies technical information about the invokers teamspeak identity on this server.

        :param event: TS3Event
        """
        cmd_prefix = '!whoami'
        if self.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            if self.can(EkkoCorePermission.WHOAMI, event):
                self.parse(UtilityParser.parse_noargs, event, cmd_prefix, event[0]['msg'],
                           description='Get technical information about your teamspeak identity on this server.')
                ictx = self.parse_invoker_context(event[0])
                self.reply(f'username: {ictx.username} | server groups: {ictx.server_groups} | '
                           f'channel group: {ictx.channel_group} | unique id: {ictx.unique_id}', event)

    def cmd_help(self, event):
        """
        Command: !help

        Lists all publicly available commands.

        :param event: TS3Event
        """
        if self.check_cmd_suitability('^!help', event[0]['msg']):
            help_cmd_strs = sorted(set(
                [str(cmd.help_cmd_str) for cmd in self.commands if cmd.help_cmd_str is not None]
            ))
            help_reply = f'List of all available command sets: \n    ' + '\n    '.join(help_cmd_strs) + \
                         '\n To receive more help about a specific command, use the `-h` or `--help` ' \
                         'flag when calling a command (e.g. !skip --help)'
            self.reply(help_reply, event)

    def cmd_permission(self, event):
        """
        Command: !permission

        Fallback command in case none of the other !permission commands catches on, replies with usage information.

        :param event: TS3Event
        """
        cmd_prefix = '!permission'
        cmd_usage = 'usage: !permission [ add | get | info | delete ]'
        if self.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            self.reply(cmd_usage, event)

    def cmd_permission_add(self, event):
        """
        Command: !permission add

        Create grants for a given permission name, based on invoker identification data (server-, channel groups, unique id)

        See `PermissionParser.parse_add` for parameters.

        :param event: TS3Event
        """
        cmd_prefix = '!permission add'
        if self.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            if self.can(EkkoCorePermission.PERMISSION_ADD, event):
                permission, uid, cg, sg, deny = self.parse(PermissionParser.parse_add, event, cmd_prefix,
                                                           event[0]['msg'],
                                                           description='Create grants for a given permission name, '
                                                                       'based on invoker identification data (server-, '
                                                                       'channel groups, unique id)')
                ictx = InvokerCtx(sg, cg, uid)
                logger.debug(ictx)
                self.permission_manager.add_grant(permission, ictx, deny)

    def cmd_permission_get(self, event):
        """
        Command: !permission get

        Lists all existing grants for a given permission name.

        See `PermissionParser.parse_get` for parameters.

        :param event: TS3Event
        """
        cmd_prefix = '!permission get'
        if self.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            if self.can(EkkoCorePermission.PERMISSION_GET, event):
                permission = self.parse(PermissionParser.parse_get, event, cmd_prefix, event[0]['msg'],
                                        description='Lists all existing grants for a given permission name.')
                p_grants = self.permission_manager.get_grant(permission)
                # FIXME: doesnt work, no idea why.
                # For now just live with the fact that you'll have to resolve them for yourself in the server group panel (manually)
                sgid_data = self.resolve_servergroups()
                logger.debug(f'sgid_data: {sgid_data}')
                grants, denies = '', ''
                logger.debug(p_grants)
                for index, grant in enumerate(p_grants):
                    if not grant.deny:
                        grants += f'\n{grant.pretty_noname_repr(sgid_data)}'
                    else:
                        denies += f'\n{grant.pretty_noname_repr(sgid_data)}'
                logger.debug(grants)
                logger.debug(denies)
                if grants or denies:
                    self.reply(f'Allowed entities: {grants or "none"}\n '
                               f'Forbidden entities: {denies or "none"}', event)
                else:
                    self.reply('no grants for this permission found.', event)

    def cmd_permission_info(self, event):
        """
        Command: !permission info

        Shows description and documentation for the given permission name.
        
        See `PermissionParser.parse_info` for parameters.

        :param event: TS3Event
        """
        cmd_prefix = '!permission info'
        if self.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            if self.can(EkkoCorePermission.PERMISSION_INFO, event):
                permisson = self.parse(PermissionParser.parse_info, event, cmd_prefix, event[0]['msg'],
                                       description='Shows description and documentation for the given permission name.')
                try:
                    perm_doc = self.permission_manager.get_grant_info(permisson)
                    self.reply(perm_doc.formatted_all, event)
                except EkkoNonexistentPermissionDoc as e:
                    self.reply(e.__str__(), event)

    def cmd_permission_delete(self, event):
        """
        Command: !permission delete

        Deletes a grant based on the given grant id.

        See `PermissionParser.parse_delete` for parameters.

        :param event: TS3Event
        """
        cmd_prefix = '!permission delete'
        if self.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            if self.can(EkkoCorePermission.PERMISSION_DELETE, event):
                permisson = self.parse(PermissionParser.parse_delete, event, cmd_prefix, event[0]['msg'],
                                       description='Deletes a grant based on the given grant id.')
                try:
                    deleted_perm = self.permission_manager.delete_grant(permisson)
                except EkkoNonexistentGrant as e:
                    self.reply(e.__str__(), event)
                else:
                    self.reply(f'grant deleted! ({deleted_perm.pretty_repr})', event)

    @staticmethod
    def color_message(text, color='#1433b1'):
        """
        Puts BB-Code formatting around the provided text.

        :param text: text which should be colored.
        :param color: the color which should be put on the text.
        :return: color BB-code formatted string.
        """
        return f'[color={color}]{text}[/color]'

    @staticmethod
    def remove_ts3_smilies(text):
        """
        Place a zero-width space inbetween characters which are transformed on display into ts3 smilies.
        
        Does not replace ':/' as this messes up the linking of [url=https://...][/url].
        
        :param text: text to be replaced in
        :return: text, but with disabled smilies
        """
        return str(text) \
            .replace(':)', ':\u200B)') \
            .replace(':D', ':\u200BD') \
            .replace('8)', '8\u200B)') \
            .replace(';)', ';\u200B)') \
            .replace(':(', ':\u200B(') \
            .replace(':C', ':\u200BC') \
            .replace(':0', ':\u200B0') \
            .replace(':x', ':\u200Bx') \
            .replace(':P', ':\u200BP')

    def determine_invoker(self, event):
        """
        Searches database for existing, matching invoker object.
        Returns found invoker or creates new object if not found.

        :param event: ts3event
        :return: Invoker object
        """
        inv = Invoker(event['invokeruid'], event['invokername'])
        inv_query = self.dbsession.query(Invoker).filter_by(unique_id=inv.unique_id, username=inv.username).first()
        if inv_query is not None:
            return inv_query
        else:
            return inv

    def resolve_servergroups(self) -> dict:
        """
        Create dataset of servergroup-ids (sgids) and their respective string name.

        FIXME: doesnt work, pls fix (ts3conn.servergrouplist() returns nothing/returns later on different notify)
        :return: dict => keys are the sgids, the data is the string name
        """
        resolved_sgids = {}
        try:
            sgid_dataset = self.ts3conn.servergrouplist()
            logger.debug(sgid_dataset.__dict__)
            for sgid_data in sgid_dataset:
                resolved_sgids[str(sgid_data['sgid'])] = sgid_data['name']
        except IndexError:
            pass
        logger.debug(resolved_sgids)
        return resolved_sgids

    def parse_invoker_context(self, event) -> InvokerCtx:
        """
        Creates InvokerCtx (Invoker Context) based on the data available in the provided event. This includes
        data like server & channel groups of the invoker, as well as their unique id.

        :param event: TS3Event
        :return: InvokerCtx()
        """
        client_id = event['invokerid']

        client_variables = self.ts3conn.clientvariable(client_id, "client_channel_group_id", "client_servergroups")[0]
        logger.debug(client_variables)
        return InvokerCtx(client_variables['client_servergroups'].split(','),
                          client_variables['client_channel_group_id'], event['invokeruid'], event['invokername'])

    @staticmethod
    def split_message(remaining_message, part_length=1024, split_chars=('\n', ' ', ''), text_mod=None):
        """
        Splits a message into parts to match a certain maximum length restriction.

        :param remaining_message: string/message which should be split
        :param part_length: maximum length of each part
        :param split_chars: characters used to split the message into parts, FIFO processing
        :param text_mod: function which transforms text (like color coding, needed to match part_length)
        :return: list of parts from the message
        """

        def dummy_text_mod(s):
            return s

        if text_mod is None:
            text_mod = dummy_text_mod

        continue_pad = '\n'
        parts = []
        # process split_chars until all parts match part_length
        for split_char in split_chars:
            while True:
                if len(remaining_message) <= 0:
                    return parts

                # split message and prepare for re-assemble
                # Also: str.split() doesnt really like to split on empty separators (like '')
                # so we need to handle that separately
                if split_char != '':
                    split_result = remaining_message.split(split_char)
                else:
                    split_result = list(remaining_message)

                stitched_message = ''
                for splitter in split_result:
                    # create imaginary part based on the current splitter and transform it in the text_mod function
                    future_part = text_mod(f'{continue_pad}{stitched_message}{splitter}{split_char}')
                    # check if this imaginary part would meet the requirement
                    if len(future_part) <= part_length:
                        stitched_message += splitter + split_char
                    else:
                        break

                if not parts and stitched_message != '':
                    # the first part should not have the continue_pad
                    # remove last appended split char again
                    if split_char != '':
                        parts.append(text_mod(stitched_message[:-len(split_char)]))
                    else:
                        # splicing with a len==0 character as length results in empty string. lets not do that.
                        parts.append(text_mod(stitched_message))
                elif stitched_message != '':
                    # remove last appended split char again
                    if split_char != '':
                        parts.append(text_mod(continue_pad + stitched_message[:-len(split_char)]))
                    else:
                        # splicing with a len==0 character as length results in empty string. lets not do that.
                        parts.append(text_mod(continue_pad + stitched_message))
                else:
                    break

                # remove processed string from remaining message
                remaining_message = remaining_message[len(stitched_message):]

    def reply(self, message, event):
        """
        Reply to the text message described by the event parameter.

        :param message: the bots message towards the other client.
        :param event: the source event to which should be replied to.
        :raises NotImplementedError: if the source event is not a text message.
        """
        if EventType.get_type(event) == EventType.TEXTMESSAGE:
            logger.debug(message)
            logger.debug(event[0])
            for message in self.split_message(message, part_length=1000, text_mod=lambda
                    s: self.color_message(self.remove_ts3_smilies(s))):
                self.ts3conn.sendtextmessage(targetmode=event[0]['targetmode'],
                                             target=event[0]['invokerid'],
                                             msg=message)
        else:
            raise NotImplementedError()
