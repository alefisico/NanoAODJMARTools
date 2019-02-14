import ROOT
import math, os, sys
import numpy as np
import fastjet
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

class nsubjettinessProducer(Module):
    def __init__(self):
        self.writeHistFile=True

        self.verbose = False
        self.maxTau = 7

        self.jetBranchName = "FatJet"
        self.rhoBranchName = "fixedGridRhoFastjetAll"
        self.pfCandsBranchName = "PFCandsAK8"

        ### Kinematics Cuts ###
        self.minJetPt = 170.
        self.maxObjEta = 2.5

        print "Load C++ Recluster worker module"
        ROOT.gSystem.Load("libPhysicsToolsNanoAODJMARTools.so")



    def beginJob(self, histFile, histDirName):
        Module.beginJob(self, histFile, histDirName)

        self.nSub1 = ROOT.NsubjettinessWrapper( 1, 0.8, 0, 6 ) ## beta, cone size, measureDef 0=Normalize, axesDef 6=onepass_kt_axes



    def endJob(self):
        Module.endJob(self)
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        jets = list(Collection(event, self.jetBranchName ))
        pfCands = list(Collection(event, self.pfCandsBranchName ))

        ### applying basic selection to jets
        recojets = [ x for x in jets if x.p4().Perp() > self.minJetPt and abs(x.p4().Rapidity()) < self.maxObjEta ]
        recojets.sort(key=lambda x:x.p4().Perp(),reverse=True)

        pfCandsVec = ROOT.vector("TLorentzVector")()
        for p in pfCands :
            pfCandsVec.push_back( ROOT.TLorentzVector( p.p4().Px(), p.p4().Py(), p.p4().Pz(), p.p4().E()) )

        for irecojet,recojet in enumerate(recojets):
            # Cluster only the particles near the appropriate jet to save time
            constituents = ROOT.vector("TLorentzVector")()
            for x in pfCandsVec:
                if recojet.p4().DeltaR( x ) < 0.8:
                    constituents.push_back(x)
            nsub1 = self.nSub1.getTau( self.maxTau, constituents )

            print '-------'
            print "On-the-fly PF jets:"
            print ' %5d: %6.2f %6.2f %6.2f %6.2f' % (irecojet, recojet.p4().Pt(), recojet.p4().Eta(), recojet.p4().Phi(), recojet.p4().M())
            for i in range(len(nsub1)): print 'tau'+str(i), round(nsub1[i], 3)


        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

