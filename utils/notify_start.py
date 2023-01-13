import config
from database import Member, Restriction
from database import db

def database_is_empty():
    if not db.get_columns("members"):
        db.create_tables([Member, Restriction])
        return True

    elif not Member.select().count():
        return True    
    
    return False

async def notify_started_bot(bot):
    await bot.send_message(config.second_group_id,"Bot successfully launched!")
