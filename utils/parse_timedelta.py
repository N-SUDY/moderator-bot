import re
import datetime as dt
from typing import Union

def parse_timedelta(specification: str) -> Union[None, dt.timedelta]:
    specification = specification.strip().replace(' ', '')
    match = re.fullmatch(r'(?:(\d+)(?:d|д))?(?:(\d+)(?:h|ч))?(?:(\d+)(?:m|м))?(?:(\d+)(?:s|с))?', specification)
    if match:
        units = [(0 if i is None else int(i)) for i in match.groups()]
        return dt.timedelta(days=units[0], hours=units[1], minutes=units[2], seconds=units[3])
    else:
        return None
