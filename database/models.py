from peewee import Model, BigIntegerField, CharField, DateField, DateTimeField, ForeignKeyField

import config
from playhouse.db_url import connect

from datetime import datetime, date

from enum import Enum
class MemberRoles(Enum):
    OWNER  = "owner"
    ADMIN  = "admin"
    HELPER = "helper"
    MEMBER = "member"


db = connect(config.db_url)

class Member(Model):
    user_id    = BigIntegerField()
    first_name = CharField()
    user_name  = CharField(null=True)
    role       = CharField()

    join_date  = DateField(default=date.today())

    reports = BigIntegerField()
    
    class Meta:
        db_table = "members"
        database = db

class Restriction(Model):
    operation   = CharField()
    
    from_admin = ForeignKeyField(Member,lazy_load=False) 
    to_user    = ForeignKeyField(Member,lazy_load=False) 

    reason      = CharField(null=True)
    date        = DateTimeField(default=datetime.now)

    class Meta:
        db_table = "restrictions"
        database = db

def build() -> None:
    db.create_tables([Member,Restriction])
