##############################################################
# WARNING: HEADER IS SKIPPED NOT PARSED, DATETIME CAN BE WRONG
# 
# https://wiki.wireshark.org/Development/LibpcapFileFormat
##############################################################

from construct import *
import time, datetime


class MicrosecAdapter(Adapter):
    def _decode(self, obj, context, path):
        return datetime.datetime.fromtimestamp(obj[0] + obj[1] / 1000000.0)
    def _encode(self, obj, context, path):
        epoch = datetime.datetime.utcfromtimestamp(0)
        return [int((obj-epoch).total_seconds()), 0]

        # offset = time.mktime(*obj.timetuple())
        # sec = int(offset)
        # usec = (offset - sec) * 1000000
        # return (sec, usec)

packet = Struct(
    "time" / MicrosecAdapter(Int32ul >> Int32ul),
    "length" / Int32ul,
    Padding(4),
    "data" / Bytes(this.length),
)

cap_file = Padded(24, GreedyRange(packet))
