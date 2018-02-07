#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODJMARTools.postprocessing.modules.jme.softdrop import *

files=[
    "test94X_NANO.root",
    ]

import random
random.seed(12345)

p1=PostProcessor(".",files,'','',[sdb0()],provenance=False, noOut=True, histFileName='sdb0.root', histDirName='sdb0', postfix='plots')

p1.run()
