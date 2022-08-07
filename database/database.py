from .models import Member,Restriction
from peewee import Field

class Database:
    def check_data_exists(self, fieldname:Field, value) -> bool | None:
        """Check if data exists in db"""
        query = Member.select().where(fieldname == value)
        
        if (query is None):
            return None

        return query.exists()
    
    def register_user(self, user_id, first_name, user_name=None, role:str='member') -> bool:
        """If the user doesn't exist, returns true. Registers a user in the db."""
        
        if self.check_data_exists(Member.user_id,user_id):
            return False

        Member.create(
            user_id    = user_id,
            first_name = first_name,
            user_name  = user_name,
            
            role       = role,

            reports    = 0,
        )     
        
        return True
    
    def search_single_member(self,fieldname:Field,value) -> Member | None:
        """If the user is found, returns dataclass. Returns user info."""
        exists = self.check_data_exists(fieldname,value)
        
        if not (exists):
            return None
        
        user = Member.get(fieldname == value)
        
        return user

    def create_restriction(self, from_user_id, to_user_id, operation, reason):
        from_admin = self.search_single_member(Member.user_id,to_user_id)
        to_user    = self.search_single_member(Member.user_id,from_user_id)
        
        if not (from_admin) or not (to_user):
            return None

        Restriction.create(
            operation = operation,
            
            from_admin = from_admin,
            to_user = to_user,
            
            reason = reason,
        ) 
    
    def search_user_restriction(self, user_id) -> list[Restriction] | None:
        user = Member.get(Member.user_id == user_id)

        query = Restriction.select().join(Member,on=Restriction.to_user)
        
        if (query is None):
            return None
        
        return query.where(Restriction.to_user == user)
    
    def delete_user(self,user_id) -> bool:
        """If the user exists, returns true. Deletes the user from the db."""

        exists = self.check_data_exists(Member.user_id,user_id)
        
        if not (exists):
            return False

        Member.delete().where(Member.user_id == user_id)

        return True
    
    def update_member_data(self, user_id, fieldnames:list[Field], newvalues:list) -> bool:
        """Update member data."""
        exists = self.check_data_exists(Member.user_id,user_id)
        
        if (not exists):
            return False
        
        for i in range(len(newvalues)):
            query = Member.update({fieldnames[i]:newvalues[i]}).where(Member.user_id == user_id)
            if (query is None):
                return False
        
        return True

    def change_reports(self,user_id,delete=False) -> int | None:
        """If the user exists, returns number reports. Gives the user a warning or retrieves it."""
        exists = self.check_data_exists(Member.user_id,user_id)
        
        if not (exists):
            return False

        count = Member.get(Member.user_id == user_id).reports

        if delete:count += 1
        else:count -= 1
        
        query = Member.update(reports = count).where(Member.user_id == user_id).execute()

        return count
