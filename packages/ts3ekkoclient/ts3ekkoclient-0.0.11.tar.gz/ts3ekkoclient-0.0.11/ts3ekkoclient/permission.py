import logging

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

try:
    from ts3ekkoclient.errors import EkkoNonexistentPermissionDoc, EkkoNonexistentGrant, PermissionDenied, \
        PermissionDuplicate
    from ts3ekkoclient.models import PermissionGrant, PermissionServerGroups, PermissionDoc, startup, desc
except ImportError:
    from .errors import EkkoNonexistentPermissionDoc, EkkoNonexistentGrant, PermissionDenied, PermissionDuplicate
    from .models import PermissionGrant, PermissionServerGroups, PermissionDoc, startup, desc

logger = logging.getLogger('ekkobot-permission')


class InvokerCtx:
    """
    Data collection about a specific user. Used to compare against other InvokerCtxs (e.g. permission restrictions)
     to determine if permission rules are matching or not.
    """

    def __init__(self, server_groups, channel_group, unique_id, username=None):
        """
        Create a new InvokerCtx object.

        :param server_groups: list of server group ids
        :param channel_group: channel group id
        :param unique_id: unique id
        :param username: (optional) username, will not be used for matching/comparing
        """
        self.server_groups = server_groups
        self.channel_group = channel_group
        self.unique_id = unique_id
        self.username = username

        if self.server_groups is not None:
            self.server_groups = [int(sgid) for sgid in self.server_groups]
        else:
            self.server_groups = []

        if self.channel_group is not None:
            self.channel_group = int(self.channel_group)

    def match(self, po):
        """
        Determine if a PermissionGrant or InvokerCtx matches with this InvokerCtx. Raises PermissionDenied if any attribute differs.
        
        :param po: PermissionGrant/InvokerCtx
        :raises PermissionDenied: on mismatch
        """
        if self.channel_group != po.channel_group and po.channel_group is not None:
            raise PermissionDenied('client_group does not match', False)
        if self.unique_id != po.unique_id and po.unique_id is not None:
            raise PermissionDenied('unique_id does not match', False)
        for server_group_o in po.server_groups or []:
            if server_group_o.server_group_id not in self.server_groups:
                raise PermissionDenied('server_groups do not match', False)

    def not_match(self, po):
        """
        Determine if a PermissionGrant or InvokerCtx does not match with this InvokerCtx. Raises PermissionDenied if no attribute differs.
        
        :param po: PermissionGrant/InvokerCtx
        :raises PermissionDenied: on full match.
        """
        if self.channel_group == po.channel_group or po.channel_group is None:
            if self.unique_id == po.unique_id or po.unique_id is None:
                for server_group_o in po.server_groups or []:
                    if server_group_o.server_group_id not in self.server_groups:
                        return
                raise PermissionDenied('client_group, unique_id and server_groups match', True)

    def __repr__(self):
        repr = f'<ts3ekkoclient.permission.InvokerCtx server_groups:"{self.server_groups}", ' \
               f'channel_group:"{self.channel_group}", unique_id: "{self.unique_id}"'
        if self.username is not None:
            repr += f', username: "{self.username}"'
        repr += '>'
        return repr


class PermissionManager:
    def __init__(self, ekko_bot, dbsession):
        self.ekko_bot = ekko_bot
        self.dbsession = dbsession

    def _find_duplicate(self, grant: PermissionGrant):
        """
        Try to find a duplicate of the given PermissionGrant. 
        Used to avoid creating multiple database-stored grants of the same InvokerCtx.
        
        :param grant: PermissionGrant which should be searched for
        :raises PermissionDuplicate: on finding another grant with the same InvokerCtx.
        """
        grant_query = self.dbsession.query(PermissionGrant).filter_by(name=grant.name, deny=grant.deny,
                                                                      channel_group=grant.channel_group,
                                                                      unique_id=grant.unique_id)
        for g in grant_query.all():
            if g == grant:
                logger.info(f'duplicate found for {grant}')
                raise PermissionDuplicate(grant)
        logger.debug(grant_query.all())

    def _query_grants(self, action: str, ictx: InvokerCtx):
        """
        Query database to find a matching grant to the given action/permission and InvokerCtx which would allow 
        the invoker to perform the requested action.
        
        If this function executes without PermissionDenied being raised, then a matching grant was found.
        
        This is the counterpart to `_query_denies`. Only if both functions are called with the same parameters 
        and do not raise the PermissionDenied error, the invoker is actually allowed for the given permission.
        
        :param action: requested permission name
        :param ictx: InvokerCtx about the invoker that requested the permission
        :raises PermissionDenied: if no matching grant could be found
        """
        grant_query = self.dbsession.query(PermissionGrant).filter_by(name=action, deny=False)
        for result in grant_query.all():
            try:
                ictx.match(result)
                logger.info(f'permission finally granted - ictx: {ictx} for action: {action}')
                return
            except PermissionDenied as e:
                logger.debug(e)
                # denied (for this rule, need to check all other rules as well)
                pass
        logger.info(f'permission finally denied - ictx: {ictx} for action: {action}')
        raise PermissionDenied('', False)

    def _query_denies(self, action: str, ictx: InvokerCtx):
        """
        Query database to find a matching deny-grant to the given action/permission and InvokerCtx which would deny 
        the invoker to perform the requested action.

        If this function executes without PermissionDenied being raised, then no matching grant was found.
        
        This is the counterpart to `_query_grants`. Only if both functions are called with the same parameters 
        and do not raise the PermissionDenied error, the invoker is actually allowed for the given permission.

        :param action: requested permission name
        :param ictx: InvokerCtx about the invoker that requested the permission
        :raises PermissionDenied: if a matching deny-grant could be found
        """
        deny_query = self.dbsession.query(PermissionGrant).filter_by(name=action, deny=True)
        for result in deny_query.all():
            try:
                ictx.not_match(result)
            except PermissionDenied:
                logger.info(f'permission finally denied (reason: blacklist)- ictx: {ictx} for action: {action}')
                raise
        logger.info(f'permission finally granted (reason: not on blacklist) - ictx: {ictx} for action: {action}')

    def add_grant(self, name: str, ictx: InvokerCtx, deny=False):
        grant = PermissionGrant()
        grant.name = name
        grant.deny = deny
        grant.unique_id = ictx.unique_id
        grant.channel_group = ictx.channel_group
        for sgid in ictx.server_groups:
            sg = PermissionServerGroups()
            sg.server_group_id = sgid
            sg.permission_grant = grant
        logger.debug(grant)
        try:
            self._find_duplicate(grant)
        except PermissionDuplicate as e:
            logger.info(e)
        else:
            self.dbsession.add(grant)
            self.dbsession.commit()

    def get_grant(self, name: str) -> list:
        """
        Returns all grants which match the name.

        :param name: Name of the grant
        :return: list of all matching grants
        """
        return self.dbsession.query(PermissionGrant).filter_by(name=name).all()

    def can(self, action: str, context: InvokerCtx) -> bool:
        """
        Checks if an action/permission is allowed in the given invoker context.
        
        :param action: requested permission name
        :param context: invoker identifications
        :return: bool depending if the action is allowed (True) or denied (False)
        """
        try:
            self._query_grants(action, context)
            self._query_denies(action, context)
        except PermissionDenied:
            return False
        else:
            return True

    def delete_grant(self, grant_id: int) -> PermissionGrant:
        """
        Delete a grant from the database, identified by their database id.
        
        :param grant_id: id of the grant to be deleted.
        :return: deleted grant if found.
        :raises EkkoNonexistentGrant: if no grant was found.
        """
        try:
            grant = self.dbsession.query(PermissionGrant).filter_by(id=grant_id).one()
            self.dbsession.delete(grant)
            return grant
        except (NoResultFound, MultipleResultsFound) as e:
            raise EkkoNonexistentGrant(grant_id)

    def get_grant_info(self, name: str) -> PermissionDoc:
        """
        Retrieve the documentation regarding the given permission name.
        
        :param name: name of the permission to look for
        :return: PermissionDoc for the found permission name
        :raises EkkoNonexistentPermissionDoc: if no documentation was found.
        """
        try:
            permdoc = self.dbsession.query(PermissionDoc).filter_by(name=name).one()
            return permdoc
        except (NoResultFound, MultipleResultsFound) as e:
            raise EkkoNonexistentPermissionDoc(name)
