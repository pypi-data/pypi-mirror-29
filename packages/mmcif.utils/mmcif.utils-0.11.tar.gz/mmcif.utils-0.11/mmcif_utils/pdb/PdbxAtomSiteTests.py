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
__author__    = "John Westbrook"
__email__     = "john.westbrook@rcsb.org"
__license__   = "Apache 2.0"
__version__   = "V0.01"

import sys, unittest, traceback

from mmcif_utils.pdb.PdbxAtomSite      import PdbxAtomSite
from mmcif.io.PdbxReader     import PdbxReader
#from mmcif.api.PdbxContainers import *

class PdbxAtomSiteTests(unittest.TestCase):
    def setUp(self):
        self.__lfh=sys.stderr
        self.__verbose=True
        self.__pathOutputFile     ="testOutputDataFile.cif"
        self.__pathPdbxDataFile   =os.path.join(HERE, "data", "1kip.cif"

    def tearDown(self):
        pass

    def testAtomSiteAniso1(self):
        """ Test 1 -  process atom site aniso records
        """
        logger.info("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            myBlockList=[]
            ifh = open(self.__pathPdbxDataFile, "r")
            pRd=PdbxReader(ifh)
            pRd.read(myBlockList)
            ifh.close()
            aS=PdbxAtomSite(verbose=self.__verbose,log=self.__lfh)
            for block in myBlockList:
                #block.printIt(self.__lfh)
                ok = aS.setAtomSiteBlock(block)
                if ok:
                    uD=aS.getAnisoTensorData()
                    #logger.info("Anisotropic data\n%r\n" % uD.items())
                    catO=aS.mergeAnisoTensorData()
                    catO.printIt(self.__lfh)
                else:
                    self.__lfh("No datablock in file %s\n" % self.__pathPdbxDataFile)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

def suite():
    return unittest.makeSuite(PdbxAtomSiteTests,'test')

if __name__ == '__main__':
    unittest.main()
