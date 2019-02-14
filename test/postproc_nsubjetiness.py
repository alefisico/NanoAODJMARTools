#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODJMARTools.postprocessing.modules.jme.nsubjettiness import *

files=[
    #"root://cmseos.fnal.gov//store/user/asparker/NanoAODJMARTools-skims//nanoskim-JetsandLepton-SingleMuon17B-trees.root",
    'root://cmseos.fnal.gov//store/user/asparker/NanoAODJMARTools-skims/nanoskim-JetsandLepton-94XMC-TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8-1of3-trees.root'
    ]

import random
random.seed(12345)

p1=PostProcessor(".",files,'','',[nsubjettinessProducer()],provenance=False, noOut=True, histFileName='nsubjettinessProducer.root', histDirName='nsubjettinessProducer', postfix='plots')

p1.run()
