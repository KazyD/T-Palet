import re

"""
in
    t : 文字列
out
    b : 文字列
"""

class CleanUp():

    def __init__(self):
        return

    def clean(self,t):
        t1 = re.sub('([あ-んア-ン一-龥ー])\s+((?=[あ-んア-ン一-龥ー]))',r'\1\2',t)
        t2 = re.match(r'(\s+)(\S+)(\s+)(.+)',t1)
        b = t2.group(2)
        return b
