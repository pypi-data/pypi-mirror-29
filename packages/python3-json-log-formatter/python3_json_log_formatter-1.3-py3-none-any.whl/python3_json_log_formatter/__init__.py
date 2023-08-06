#!/usr/bin/env python3
"""
This file is part of json_log_formatter.

json_log_formatter is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

json_log_formatter is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with json_log_formatter.  If not, see <http://www.gnu.org/licenses/>.
"""

from logging import Formatter
from json import (dumps, loads)
from datetime import (
    datetime
)


class JsonFormatter(Formatter):

    def __init__(self, attributes=None, json_kwargs=None,
                 resolve_args=True, datefmt=None, style='%'):
        """ Construct a new JSON formatter

        :param attributes: Attributes of the log object to include.
            Default is `None`, which means include all attributes.

        :param json_kwargs: Keyword arguments directly passed into
            `json.dumps()`

        :param datefmt: Date format. See Python docs.

        :param style: Formatter style. See Python docs.

        :param resolve_args: Whether to inject `args` into `message`. Default
            is `True`. Setting to `False` will result in the json log entry
            to include both a `msg` and `args` item.
        """
        self.attributes = attributes
        self.json_kwargs = json_kwargs or {'indent': 2}
        self.resolve_args = resolve_args
        if 'indent' not in self.json_kwargs:
            self.json_kwargs['indent'] = 2
        super(JsonFormatter, self).__init__(datefmt=datefmt, style=style)

    def lets_make_a_date(self, timestamp):
        if not self.datefmt:
            return timestamp
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime(self.datefmt)

    def format(self, record):
        data = {}
        for (a, v) in record.__dict__.items():
            if self.attributes is not None and a not in self.attributes:
                continue
            if any((a.startswith('_'), )):
                continue
            try:
                v2 = dict(v)
                data[a] = dumps(v2, **(self.json_kwargs or {}))
            except Exception as e:
                pass
            try:
                v2 = loads(v)
                data[a] = dumps(v2, **(self.json_kwargs or {}))
            except Exception as e:
                pass

            if isinstance(v, (float, int, bool)):
                data[a] = v
            elif isinstance(v, (list, tuple, set)):
                data[a] = type(v)([str(x) for x in v])
            elif isinstance(v, dict):
                data[a] = type(v)([(x, str(y)) for (x, y) in v.items()])
            else:
                data[a] = str(v).replace('\\\\', '\\')
        if self.resolve_args:
            data['msg'] = data['msg'] % data['args']
            del data['args']
        # Format the dates
        for k in ('created', ):
            data[k] = self.lets_make_a_date(data[k])
        # data['created'] = self.lets_make_a_date(data['created'])
        # Format the messages
        return dumps(data, **(self.json_kwargs or {})).replace('\\\\', '\\')
