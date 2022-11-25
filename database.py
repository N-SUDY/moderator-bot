from peewee import Field, Model, BigIntegerField, CharField, DateField, DateTimeField, ForeignKeyField

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
    username  = CharField(null=True)
    
    warns = BigIntegerField(default=0)
    
    role = CharField(default="member")
    
    joined  = DateField(default=date.today())
    
    
    @staticmethod
    def exists(fieldname, value) -> bool | None:
        """Check if data exists in db"""
        query = Member.select().where(fieldname == value)
        
        if (query is None):
            return None

        return query.exists()

    @staticmethod
    def search(fieldname:Field, value):
        if (not Member.exists(fieldname, value)):
            return None
        
        return Member.get(fieldname == value)
    
    @staticmethod
    def report(delete=False):
        """If the user exists, returns number reports. Gives the user a warning or retrieves it."""
        count = Member.warns

        if delete:count -= 1
        else:count += 1
        
        Member.update(warns = count).execute()

        return count

    class Meta:
        db_table = "members"
        database = db

class Restriction(Model):
    action     = CharField()
    
    from_user  = ForeignKeyField(Member, lazy_load=True) 
    to_user    = ForeignKeyField(Member, lazy_load=True) 

    reason      = CharField(null=True)
    timestamp   = DateTimeField(default=datetime.now().replace(microsecond=0))
    
    @staticmethod
    def search(to_user=None,id=None):
        if (id):
            query = Restriction.get(Restriction.id == id)
        if (to_user):
            query = Restriction.select().where(Restriction.to_user == to_user)
        
        return query
    
    class Meta:
        db_table = "auditlog"
        database = db

# if not db.get_columns('members'):
#     db.create_tables([Member,Restriction])
#     logging.warning("Members table is empty, you need get data(run !reload)")
#
# if Member.select().count() == 0:
#     logging.warning("Members table is empty, you need get data(run !reload)")

# def build() -> None:
#     db.create_tables([Member,Restriction])
