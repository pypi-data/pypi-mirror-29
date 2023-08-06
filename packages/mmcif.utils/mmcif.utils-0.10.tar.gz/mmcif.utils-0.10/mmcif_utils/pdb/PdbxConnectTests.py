##
#File:    PdbxConnectTests.py
#Author:  jdw
#Date:    5-June-2010
#Version: 0.001
#
# Updated:
#  23-Oct-2012 jdw  Update path and reorganize
##


__docformat__ = "restructuredtext en"
__author__    = "John Westbrook"
__email__     = "john.westbrook@rcsb.org"
__license__   = "Apache 2.0"
__version__   = "V0.01"


import sys, unittest, traceback
import sys, time, os, os.path, shutil

from mmcif_utils.pdb.PdbxConnect     import PdbxConnect
from mmcif.io.PdbxReader   import PdbxReader
#from mmcif.api.PdbxContainers import *

class PdbxConnectTests(unittest.TestCase):
    def setUp(self):
        self.__lfh=sys.stderr
        self.__verbose=True
        self.__pathOutputFile     ="testOutputDataFile.cif"
        self.__topCachePath='/data/components/ligand-dict-v3'
        self.__pathPdbxDataFile      =os.path.join(HERE, "data", "1kip.cif"

    def tearDown(self):
        pass

    def testConnect1(self):
        """Test case -  process atom site records
        """
        logger.info("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            myBlockList=[]
            ifh = open(self.__pathPdbxDataFile, "r")
            pRd=PdbxReader(ifh)
            pRd.read(myBlockList)
            ifh.close()
            cCon=PdbxConnect(topCachePath=self.__topCachePath,verbose=self.__verbose,log=self.__lfh)
            for block in myBlockList:
                ok = cCon.setAtomSiteBlock(block)
                if ok:
                    cCon.getLinkData()
                    cCon.getNonStandardDataAndLinks()
                    cCat=cCon.getConnect()
                    block.printIt(self.__lfh)
                else:
                    self.__lfh("No datablock in file %s\n" % self.__pathPdbxDataFile)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

def suite():
    return unittest.makeSuite(PdbxConnectTests,'test')

if __name__ == '__main__':
    unittest.main()
