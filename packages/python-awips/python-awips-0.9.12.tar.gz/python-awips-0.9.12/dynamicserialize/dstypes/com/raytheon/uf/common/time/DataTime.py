# #
# #

# File auto-generated against equivalent DynamicSerialize Java class
# and then modified post-generation to add additional features to better
# match Java implementation.
#
#     SOFTWARE HISTORY
#
#    Date            Ticket#       Engineer       Description
#    ------------    ----------    -----------    --------------------------
#    ??/??/??                      xxxxxxxx       Initial Creation.
#    05/28/13         2023         dgilling       Implement __str__().
#    01/22/14         2667         bclement       preserved milliseconds in string representation
#    03/03/14         2673         bsteffen       allow construction using a Date for refTime
#    06/24/14         3096         mnash          implement __cmp__
#    06/24/15         4480         dgilling       implement __hash__ and __eq__,
#                                                 replace __cmp__ with rich comparison
#                                                 operators.
#

import calendar
import datetime
import numpy
import time
from six.moves import cStringIO as StringIO

from dynamicserialize.dstypes.java.util import Date
from dynamicserialize.dstypes.java.util import EnumSet

from .TimeRange import TimeRange

class DataTime(object):

    def __init__(self, refTime=None, fcstTime=None, validPeriod=None):
        self.fcstTime = int(fcstTime) if fcstTime is not None else 0
        self.refTime = refTime if refTime is not None else None
        if validPeriod is not None and type(validPeriod) is not TimeRange:
            ValueError("Invalid validPeriod object specified for DataTime.")
        self.validPeriod = validPeriod if validPeriod is not None else None
        self.utilityFlags = EnumSet('com.raytheon.uf.common.time.DataTime$FLAG')
        self.levelValue = numpy.float64(-1.0)

        if self.refTime is not None:
            if isinstance(self.refTime, datetime.datetime):
                self.refTime = int(calendar.timegm(self.refTime.utctimetuple()) * 1000)
            elif isinstance(self.refTime, time.struct_time):
                self.refTime = int(calendar.timegm(self.refTime) * 1000)
            elif hasattr(self.refTime, 'getTime'):
                # getTime should be returning ms, there is no way to check this
                # This is expected for java Date
                self.refTime = int(self.refTime.getTime())
            else:
                self.refTime = int(refTime)
            self.refTime = Date(self.refTime)

            if self.validPeriod is None:
                validTimeMillis = self.refTime.getTime() + int(self.fcstTime * 1000)
                self.validPeriod = TimeRange()
                self.validPeriod.setStart(validTimeMillis / 1000)
                self.validPeriod.setEnd(validTimeMillis / 1000)

        # figure out utility flags
        if fcstTime:
            self.utilityFlags.add("FCST_USED")
        if self.validPeriod and self.validPeriod.isValid():
            self.utilityFlags.add("PERIOD_USED")

    def getRefTime(self):
        return self.refTime

    def setRefTime(self, refTime):
        self.refTime = refTime

    def getFcstTime(self):
        return self.fcstTime

    def setFcstTime(self, fcstTime):
        self.fcstTime = fcstTime

    def getValidPeriod(self):
        return self.validPeriod

    def setValidPeriod(self, validPeriod):
        self.validPeriod = validPeriod

    def getUtilityFlags(self):
        return self.utilityFlags

    def setUtilityFlags(self, utilityFlags):
        self.utilityFlags = utilityFlags

    def getLevelValue(self):
        return self.levelValue

    def setLevelValue(self, levelValue):
        self.levelValue = numpy.float64(levelValue)

    def __str__(self):
        buffer = StringIO()

        if self.refTime is not None:
            refTimeInSecs = self.refTime.getTime() / 1000
            micros = (self.refTime.getTime() % 1000) * 1000
            dtObj = datetime.datetime.utcfromtimestamp(refTimeInSecs)
            dtObj = dtObj.replace(microsecond=micros)
            buffer.write(dtObj.isoformat(' '))

        if "FCST_USED" in self.utilityFlags:
            hrs = int(self.fcstTime / 3600)
            mins = int((self.fcstTime - (hrs * 3600)) / 60)
            buffer.write(" (" + str(hrs))
            if mins != 0:
                buffer.write(":" + str(mins))
            buffer.write(")")

        if "PERIOD_USED" in self.utilityFlags:
            buffer.write("[")
            buffer.write(self.validPeriod.start.isoformat(' '))
            buffer.write("--")
            buffer.write(self.validPeriod.end.isoformat(' '))
            buffer.write("]")

        strVal = buffer.getvalue()
        buffer.close()
        return strVal

    def __repr__(self):
        return "<DataTime instance: " + str(self) + " >"

    def __hash__(self):
        hashCode = hash(self.refTime) ^ hash(self.fcstTime)
        if self.validPeriod is not None and self.validPeriod.isValid():
            hashCode ^= hash(self.validPeriod.getStart())
            hashCode ^= hash(self.validPeriod.getEnd())
        hashCode ^= hash(self.levelValue)
        return hashCode

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if other.getRefTime() is None:
            return self.fcstTime == other.fcstTime

        dataTime1 = (self.refTime, self.fcstTime, self.validPeriod, self.levelValue)
        dataTime2 = (other.refTime, other.fcstTime, other.validPeriod, other.levelValue)
        return dataTime1 == dataTime2

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if type(self) != type(other):
            return NotImplemented

        myValidTime = self.getRefTime().getTime() + self.getFcstTime()
        otherValidTime = other.getRefTime().getTime() + other.getFcstTime()
        if myValidTime < otherValidTime:
            return True

        if self.fcstTime < other.fcstTime:
            return True

        if self.levelValue < other.levelValue:
            return True

        myValidPeriod = self.validPeriod
        otherValidPeriod = other.validPeriod
        if myValidPeriod != otherValidPeriod:
            if myValidPeriod.duration() < otherValidPeriod.duration():
                return True
            return myValidPeriod.getStartInMillis() < otherValidPeriod.getStartInMillis()
        return False

    def __le__(self, other):
        if type(self) != type(other):
            return NotImplemented

        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        if type(self) != type(other):
            return NotImplemented

        myValidTime = self.getRefTime().getTime() + self.getFcstTime()
        otherValidTime = other.getRefTime().getTime() + other.getFcstTime()
        if myValidTime > otherValidTime:
            return True

        if self.fcstTime > other.fcstTime:
            return True

        if self.levelValue > other.levelValue:
            return True

        myValidPeriod = self.validPeriod
        otherValidPeriod = other.validPeriod
        if myValidPeriod != otherValidPeriod:
            if myValidPeriod.duration() > otherValidPeriod.duration():
                return True
            return myValidPeriod.getStartInMillis() > otherValidPeriod.getStartInMillis()
        return False

    def __ge__(self, other):
        if type(self) != type(other):
            return NotImplemented

        return self.__gt__(other) or self.__eq__(other)
