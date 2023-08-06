##
# File:    PdbxAnnFeatureTests.py
# Author:  jdw
# Date:    17-Feb-2012
# Version: 0.001
#
# Updated:
#        23-Oct-2012 jdw  Update path and reorganize
##

"""
Unit tests for classes supporting annotation feature data files.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"
__version__ = "V0.01"


import sys
import unittest
import time
import os

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

from mmcif_utils.pdb.PdbxAnnFeature import PdbxAnnFeatureReader, PdbxAnnFeatureUpdater


class PdbxAnnFeatureTests(unittest.TestCase):

    def setUp(self):
        self.__lfh = sys.stderr
        self.__verbose = True
        self.__pathInputFile = os.path.join(HERE, "data", "carbohydrate_features_1.cif")
        self.__pathOutputFile = os.path.join(HERE, "test-output", "testAnnFeatureUpdFile.cif")
        self.__pathOutputFile2 = os.path.join(HERE, "test-output", "testAnnFeatureOutFile.cif")
        self.__startTime = time.time()
        logger.debug("Running tests on version %s" % __version__)
        logger.debug("Starting %s at %s" % (self.id(),
                                            time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)\n" % (self.id(),
                                                              time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                              endTime - self.__startTime))

    def testGetCategories(self):
        """Test case -  get categories --
        """
        try:
            prd = PdbxAnnFeatureReader(verbose=self.__verbose)
            prd.setFilePath(self.__pathInputFile)
            prd.get()
            catList = prd.getCategoryList()
            logger.debug("Category list %r\n" % catList)
            for catName in catList:
                dL = prd.getCategory(catName)
                logger.debug("Category %r\n" % dL)
            self.assertGreaterEqual(len(catList), 100)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testUpdateReadWrite(self):
        """Test case -  read/write
        """
        try:
            prd = PdbxAnnFeatureUpdater(verbose=self.__verbose)
            prd.read(self.__pathInputFile)
            catList = prd.getCategoryList()
            logger.debug("Categories: %r\n" % catList)
            prd.writeFile(filePath=self.__pathOutputFile)
            self.assertGreaterEqual(len(catList), 100)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()


def suite():
    return unittest.makeSuite(PdbxAnnFeatureTests, 'test')

if __name__ == '__main__':
    unittest.main()
