from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, create_engine, desc, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import logging

Base = declarative_base()


class TextAlias(Base):
    __tablename__ = 'textalias'
    # Internal ID
    id = Column(Integer, Sequence('textalias_id_seq', start=1001, increment=1), primary_key=True)
    # Alias (keyword)
    alias = Column(String(1024), nullable=False)
    # Associated value which should replace the alias
    value = Column(String(2048))
    # Timestamp on which this entry was created
    timestamp = Column(DateTime, nullable=False)
    invoker_id = Column(Integer, ForeignKey('invoker.id'))
    invoker = relationship('Invoker', back_populates='textalias')

    def __repr__(self):
        return f'<ts3ekkoclient.models.TextAlias id={self.id}, alias={self.alias}, value={self.value}, ' \
               f'timestamp={self.timestamp}, invoker={self.invoker_id}>'

    @property
    def is_deleted(self):
        return self.value is None or self.value == ''


class MediaAlias(Base):
    __tablename__ = 'mediaalias'
    # Internal ID
    id = Column(Integer, Sequence('mediaalias_id_seq', start=1001, increment=1), primary_key=True)
    # Alias (keyword)
    alias = Column(String(1024), nullable=False)
    # Associated value which should replace the alias
    value = Column(String(2048))
    # Timestamp on which this entry was created
    timestamp = Column(DateTime, nullable=False)
    invoker_id = Column(Integer, ForeignKey('invoker.id'))
    invoker = relationship('Invoker', back_populates='mediaalias')

    def __repr__(self):
        return f'<ts3ekkoclient.models.MediaAlias id={self.id}, alias={self.alias}, value={self.value}, ' \
               f'timestamp={self.timestamp}, invoker={self.invoker_id}>'

    @property
    def is_deleted(self):
        return self.value is None or self.value == ''


class Invoker(Base):
    __tablename__ = 'invoker'
    # Internal ID
    id = Column(Integer, Sequence('invoker_id_seq', start=1001, increment=1), primary_key=True)

    textalias = relationship('TextAlias', back_populates='invoker')
    mediaalias = relationship('MediaAlias', back_populates='invoker')

    # Creators unique_id, required because usernames can be "spoofed"
    unique_id = Column(String(50), nullable=False)
    # For convenience also include username because reversing unique_id may require more privileges
    username = Column(String(50), nullable=False)

    def __init__(self, unique_id, username, id=None):
        self.unique_id = unique_id
        self.username = username

        if id is not None:
            self.id = id

    @property
    def is_mediainvoker(self):
        return self.media_alias is not None

    @property
    def is_textinvoker(self):
        return self.text_alias is not None


class PermissionServerGroups(Base):
    __tablename__ = 'permission_server_groups'
    id = Column(Integer, Sequence('permission_server_groups_id_seq', start=1001, increment=1), primary_key=True)
    server_group_id = Column(Integer, nullable=False)
    permission_grant_id = Column(Integer, ForeignKey('permission_grant.id'))
    permission_grant = relationship('PermissionGrant', back_populates='server_groups')

    def __eq__(self, other):
        return self.server_group_id == other.server_group_id and \
               self.permission_grant_id == other.permission_grant_id

    def __ne__(self, other):
        return not self.server_group_id == other.server_group_id and \
               self.permission_grant_id == other.permission_grant_id

    def __repr__(self):
        return f'<ts3ekkoclient.models.PermissionServerGroups id={self.id}, server_group={self.server_group_id}>'


class PermissionGrant(Base):
    __tablename__ = 'permission_grant'
    id = Column(Integer, Sequence('permission_grant_id_seq', start=1001, increment=1), primary_key=True)
    name = Column(String, nullable=False)
    deny = Column(Boolean, default=False)

    server_groups = relationship('PermissionServerGroups', back_populates='permission_grant')
    channel_group = Column(Integer)
    unique_id = Column(String(50))

    @property
    def server_group_set(self):
        return set([sg.server_group_id for sg in self.server_groups])

    def __eq__(self, other):
        return self.channel_group == other.channel_group and \
               self.unique_id == other.unique_id and \
               self.server_group_set == other.server_group_set

    def __ne__(self, other):
        return not self.channel_group == other.channel_group and \
               self.unique_id == other.unique_id and \
               self.server_group_set == other.server_group_set

    def __repr__(self):
        return f'<ts3ekkoclient.models.PermissionGrant id={self.id}, deny={self.deny}, name={self.name} ' \
               f'channel_group={self.channel_group}, unique_id={self.unique_id}, ' \
               f'server_groups={self.server_groups}, prop:server_group_set={self.server_group_set}>'

    @property
    def pretty_repr(self):
        return f'<Grant deny={self.deny}, name={self.name} ' \
               f'channel_group={self.channel_group}, unique_id={self.unique_id}, ' \
               f'server_groups={self.server_group_set}>'

    def pretty_noname_repr(self, sgid_data=None):
        logging.debug(sgid_data)
        server_groups_resolved = []
        for sgid in self.server_group_set:
            try:
                server_groups_resolved.append(str(sgid_data[sgid]))
            except KeyError:
                server_groups_resolved.append(str(sgid))

        output = f'(id={self.id}): Channel Group: {self.channel_group or "any"}, '
        logging.debug(output)
        if server_groups_resolved:
            output += f'Server Groups: {",".join(sorted(server_groups_resolved))}, '
        else:
            output += f'Server Groups: any, '

        if self.unique_id:
            output += f'Unique ID: {self.unique_id}'
        logging.debug(output)
        return output


class PermissionDoc(Base):
    __tablename__ = 'permission_doc'
    id = Column(Integer, Sequence('permission_doc_id_seq', start=1001, increment=1), primary_key=True)
    name = Column(String, nullable=False, unique=True)
    short_description = Column(String)
    long_description = Column(String)

    @property
    def formatted_long(self):
        return f'\npermission: {self.name}\n\n{self.long_description or ""}'

    @property
    def formatted_short(self):
        return f'\npermission: {self.name}\n\n{self.short_description or ""}'

    @property
    def formatted_all(self):
        return f'\npermission: {self.name}\n\n{self.short_description or ""}\n\n{self.long_description or ""}'


def startup(username='ekko', password='ekkopassword', dbhost='dbhost', dbname='ekkodb'):
    engine = create_engine(f'postgres://{username}:{password}@{dbhost}/{dbname}')

    Base.metadata.create_all(engine)

    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)

    session = DBSession()
    return session
