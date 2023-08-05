import datetime
import json
from time import mktime


class TrellioEncoder(json.JSONEncoder):
    """
    json dump encoder class
    """

    def default(self, obj):
        """
        convert datetime instance to str datetime
        """
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))
        return json.JSONEncoder.default(self, obj)
