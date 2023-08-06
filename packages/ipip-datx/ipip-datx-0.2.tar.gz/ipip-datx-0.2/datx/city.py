# -*- coding: utf-8 -*-  
"""
    :copyright: ©2018 by IPIP.net
"""

import sys
import os

def ip2long(ip):
    a = ip.split(".")
    return int(a[0]) << 24 | int(a[1]) << 16 | int(a[2]) << 8 | int(a[3])


def bytes2long(a, b, c, d):
    return convert(a) << 24 | convert(b) << 16 | convert(c) << 8 | convert(d)

def convert(v):
    if sys.version_info.major >= 3:
        return v
    else:
        return ord(v)
            

class City:
    
    data = b""
    indexSize = 0

    def __init__(self, name):
        file = open(name, "rb")
        self.data = file.read()
        file.close()
        self.indexSize = bytes2long((self.data[0]), (self.data[1]), (self.data[2]), (self.data[3]))

    def find(self, ip):
        low = 0
        mid = 0
        high = int((self.indexSize - 262144 - 262148) / 9) - 1
        pos = 0
        val = ip2long(ip)

        while (low <= high):
            mid = int((low + high) / 2)
            pos = mid * 9 + 262148
            start = 0
            if mid > 0 :
                pos1 = (mid - 1) * 9 + 262148
                start = bytes2long(
                    (self.data[pos1]), 
                    (self.data[pos1+1]), 
                    (self.data[pos1+2]), 
                    (self.data[pos1+3])
                )
                start = start + 1

            end = bytes2long(
                self.data[pos], 
                self.data[pos+1], 
                self.data[pos+2], 
                self.data[pos+3]
            )

            if val < start :
                high = mid - 1
            elif val > end:
                low = mid + 1
            else:
                b = 0;
                off = convert(self.data[pos+6]) << 16 | convert(self.data[pos+5]) << 8 | convert(self.data[pos+4]);

                l = convert(self.data[pos+7]) << 8 | convert(self.data[pos+8]);

                pos = off - 262144 + self.indexSize;

                tmp = (self.data[pos:pos+l]).decode("utf-8")

                return tmp.split("\t")