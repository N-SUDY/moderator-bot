import re
import typing

import datetime

from load import types


def parse_timedelta(value: str) -> typing.Optional[datetime.timedelta]:
    specification = value.strip().replace(' ', '')
    match = re.fullmatch(r'(?:(\d+)(?:d|д))?(?:(\d+)(?:h|ч))?(?:(\d+)(?:m|м))?(?:(\d+)(?:s|с))?', specification)
    if match:
        units = [(0 if i is None else int(i)) for i in match.groups()]
        return datetime.timedelta(days=units[0], hours=units[1], minutes=units[2], seconds=units[3])
    else:
        return None


async def parse_timedelta_from_message(
        message: types.Message,
    ) -> typing.Optional[datetime.timedelta]:
        _, *args = message.text.split()
        
        if args:
            duration = re.findall(r"(\d+d|\d+h|\d+m|\d+s)",''.join(message.text))
            duration = " ".join(duration)
            duration = parse_timedelta(duration)
            
            return duration
        else:    
            return datetime.timedelta(0,0,0) # forever
