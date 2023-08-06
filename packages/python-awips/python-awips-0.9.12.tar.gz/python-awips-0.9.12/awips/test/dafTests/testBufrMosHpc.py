##
##

from __future__ import print_function
from awips.dataaccess import DataAccessLayer as DAL

import baseBufrMosTestCase
import unittest

#
# Test DAF support for bufrmosHPC data
#
#     SOFTWARE HISTORY
#
#    Date            Ticket#       Engineer       Description
#    ------------    ----------    -----------    --------------------------
#    01/19/16        4795          mapeters       Initial Creation.
#    04/11/16        5548          tgurney        Cleanup
#    04/18/16        5548          tgurney        More cleanup
#
#


class BufrMosHpcTestCase(baseBufrMosTestCase.BufrMosTestCase):
    """Test DAF support for bufrmosHPC data"""

    datatype = "bufrmosHPC"

    # Most tests inherited from superclass

    def testGetGeometryData(self):
        req = DAL.newDataRequest(self.datatype)
        req.setLocationNames("KOMA")
        req.setParameters("forecastHr", "maxTemp24Hour")
        self.runGeometryDataTest(req)
