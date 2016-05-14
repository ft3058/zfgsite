# coding:utf8
"""

"""

import re

s = 'abc - 12.3.4.194 - cde'

ip_candidates = re.findall(r".*\d{1, 3}\.\d{1, 3}\.\d{1, 3}\.\d{1, 3}.*", s)

print ip_candidates