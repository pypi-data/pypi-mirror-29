##
# File:    PdbxAtomSiteTests.py
# Author:  jdw
# Date:    23-Mar-2011
# Version: 0.001
#
# Updated:
#  23-Oct-2012 jdw  Update path and reorganize
#
##
"""
Test cases for processing and merging atom records.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"

import os
import sys
import time
import unittest

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s')
logger = logging.getLogger()

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

try:
    from mmcif_utils import __version__
except Exception as e:
    sys.path.insert(0, TOPDIR)
    from mmcif_utils import __version__


from mmcif_utils.pdb.PdbxAtomSite import PdbxAtomSite
from mmcif.io.PdbxReader import PdbxReader


class PdbxAtomSiteTests(unittest.TestCase):

    def setUp(self):
        self.__lfh = sys.stderr
        self.__verbose = True
        self.__pathOutputFile = os.path.join(HERE, "test-output", "testOutputDataFile.cif")
        self.__pathPdbxDataFile = os.path.join(HERE, "data", "1kip.cif")
        self.__startTime = time.time()
        logger.debug("Running tests on version %s" % __version__)
        logger.debug("Starting %s at %s" % (self.id(),
                                            time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)\n" % (self.id(),
                                                              time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                              endTime - self.__startTime))

    def testAtomSiteAniso1(self):
        """ Test 1 -  process atom site aniso records
        """
        try:
            myBlockList = []
            ifh = open(self.__pathPdbxDataFile, "r")
            pRd = PdbxReader(ifh)
            pRd.read(myBlockList)
            ifh.close()
            aS = PdbxAtomSite(verbose=self.__verbose)
            for block in myBlockList:
                # block.printIt(self.__lfh)
                ok = aS.setAtomSiteBlock(block)
                if ok:
                    uD = aS.getAnisoTensorData()
                    # logger.info("Anisotropic data\n%r\n" % uD.items())
                    catO = aS.mergeAnisoTensorData()
                    catO.printIt(self.__lfh)
                else:
                    logger.warning("No datablock in file %s\n" % self.__pathPdbxDataFile)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()


def suite():
    return unittest.makeSuite(PdbxAtomSiteTests, 'test')

if __name__ == '__main__':
    unittest.main()
