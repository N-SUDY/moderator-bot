import re
from typing import Optional

import datetime
from load import types


def parse_timedelta(value: str) -> Optional[datetime.timedelta]:
    regex = r'(?:(\d+)(?:d|д))?(?:(\d+)(?:h|ч))?(?:(\d+)(?:m|м))?(?:(\d+)(?:s|с))?'
    specification = value.strip().replace(' ', '')
    match = re.fullmatch(regex, specification)
    if match:
        units = [(0 if i is None else int(i)) for i in match.groups()]
        return datetime.timedelta(
            days=units[0],
            hours=units[1],
            minutes=units[2],
            seconds=units[3]
        )


def parse_timedelta_from_message(message: types.Message) -> Optional[datetime.timedelta]:
    _, *args = message.text.split()
        
    if args:
        duration = re.findall(r"(\d+d|\d+h|\d+m|\d+s)", ''.join(message.text))
        if duration:
            duration = " ".join(duration)
            duration = parse_timedelta(duration)
        if not duration:
            duration = datetime.timedelta(0, 0, 0)
        return duration
