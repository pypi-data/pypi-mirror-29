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
__author__    = "John Westbrook"
__email__     = "john.westbrook@rcsb.org"
__license__   = "Apache 2.0"
__version__   = "V0.01"


import sys, unittest, traceback
import sys, time, os, os.path, shutil

from mmcif_utils.pdb.PdbxAnnFeature    import PdbxAnnFeatureCategoryDefinition
from mmcif_utils.pdb.PdbxAnnFeature    import PdbxAnnFeatureReader,PdbxAnnFeatureUpdater
#from mmcif.api.PdbxContainers import *
from mmcif.io.PdbxWriter     import PdbxWriter


class PdbxAnnFeatureTests(unittest.TestCase):
    def setUp(self):
        self.__lfh=sys.stderr
        self.__verbose=True
        self.__pathInputFile       =os.path.join(HERE, "data", "carbohydrate_features_1.cif"
        self.__pathOutputFile      ="testAnnFeatureUpdFile.cif"
        self.__pathOutputFile2     ="testAnnFeatureOutFile.cif"

    def tearDown(self):
        pass

    def testGetCategories(self):
        """Test case -  categories --
        """
        logger.info("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            cI=PdbxAnnFeatureCategoryDefinition._categoryInfo
            prd=PdbxAnnFeatureReader(verbose=self.__verbose,log=self.__lfh)
            prd.setFilePath(self.__pathInputFile)
            prd.get()
            catList=prd.getCategoryList()
            logger.info("Category list %r\n" % catList)
            for catName in catList:
                dL=prd.getCategory(catName)
                logger.info("Category %r\n" % dL)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testUpdateReadWrite(self):
        """Test case -  read/write
        """
        logger.info("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            cI=PdbxAnnFeatureCategoryDefinition._categoryInfo
            prd=PdbxAnnFeatureUpdater(verbose=self.__verbose,log=self.__lfh)
            prd.read(self.__pathInputFile)
            catList=prd.getCategoryList()
            logger.info("Categories: %r\n" % catList)
            prd.writeFile(filePath=self.__pathOutputFile)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()




def suite():
    return unittest.makeSuite(PdbxAnnFeatureTests,'test')

if __name__ == '__main__':
    unittest.main()
