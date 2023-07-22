from peewee import CharField, BigIntegerField, DateField, DateTimeField, ForeignKeyField

from enum import Enum
import config
from playhouse.db_url import connect

from datetime import datetime, date
from peewee import Model

db = connect(config.db_uri)


class MemberRoles(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    HELPER = "helper"
    MEMBER = "member"


class Member(Model):
    user_id = BigIntegerField()
    first_name = CharField()
    username = CharField(null=True)
    
    role = CharField(default="member")

    warns = BigIntegerField(default=0)
    
    joined = DateField(default=date.today())
    
    class Meta:
        db_table = "members"
        database = db


class Restriction(Model):
    from_user = ForeignKeyField(Member, lazy_load=True)
    to_user = ForeignKeyField(Member, lazy_load=True)

    text = CharField()
    message_id = BigIntegerField()
    timestamp = DateTimeField(default=datetime.now().replace(microsecond=0))
    
    class Meta:
        db_table = "auditlog"
        database = db
