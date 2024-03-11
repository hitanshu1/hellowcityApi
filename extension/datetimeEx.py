
from datetime import datetime

def to_datetime(string, date_format='%Y-%m-%d %H:%M:%S'):
    if string is not None:
        return datetime.strptime(string, date_format)
    else :
        return None