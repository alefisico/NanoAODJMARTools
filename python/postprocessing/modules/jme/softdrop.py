import ROOT
import math, os
import numpy as np
import fastjet
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import matchObjectCollection

class softDropProducer(Module):
    def __init__(self, beta=0.0, zcut=0.1, bname="sdb0"):
        self.writeHistFile=True
        
        
        self.beta = beta
        self.zcut = zcut
        self.jetBranchName = "FatJet"
        self.genJetBranchName = "GenJetAK8"
        self.rhoBranchName = "fixedGridRhoFastjetAll"
        self.pfCandsBranchName = "PFCandsAK8"
        self.genCandsBranchName = "GenPartAK8"
        self.bname = bname
        
        print "Load C++ Recluster worker module"                
        ROOT.gSystem.Load("libPhysicsToolsNanoAODJMARTools.so")
                
        

    def beginJob(self, histFile, histDirName):
        self.sd = ROOT.SoftDropWrapper(self.beta,self.zcut)
        Module.beginJob(self, histFile, histDirName)
        self.addObject(ROOT.TH1F('h_ak8sdm_'+self.bname,   'h_ak8sdm_'+self.bname, 25, 0, 250) )


    def endJob(self):
        Module.endJob(self)
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        #jets = Collection(event, self.jetBranchName )
        #genJets = Collection(event, self.genJetBranchName )
        pfCands = Collection(event, self.pfCandsBranchName )
        genCands = Collection(event, self.genCandsBranchName )

        pfCandsVec = ROOT.vector("TLorentzVector")()
        for p in pfCands :
            pfCandsVec.push_back( ROOT.TLorentzVector( p.p4().Px(), p.p4().Py(), p.p4().Pz(), p.p4().E()) )
        sdjets = self.sd.result( pfCandsVec )

        genCandsVec = ROOT.vector("TLorentzVector")()
        for p in genCands :
            genCandsVec.push_back( ROOT.TLorentzVector( p.p4().Px(), p.p4().Py(), p.p4().Pz(), p.p4().E()) )
        gensdjets = self.sd.result( genCandsVec )

        

        if len(pfCands) == 0 :
            return False
        print 'Event : ', event.event
        
        ## print "NANOAOD PF jets:"
        ## for i,jet in enumerate(jets):
        ##     print ' %5d: %6.2f %6.2f %6.2f %6.2f %6.2f' % (i, jet.pt, jet.eta, jet.phi, jet.mass, jet.msoftdrop)
        print '-------'            
        print "On-the-fly PF jets:"
        for i,sdjet in enumerate(sdjets):
            print ' %5d: %6.2f %6.2f %6.2f %6.2f' % (i, sdjet.perp(), sdjet.eta(), sdjet.phi(), sdjet.m())
            print 'Subjets:'
            subs = sdjet.pieces()
            for j,sub in enumerate(subs):
                print '      : %6.2f %6.2f %6.2f %6.2f' % (sub.perp(), sub.eta(), sub.phi(), sub.m())

        print '-------'

        ## print "NANOAOD Gen jets:"
        ## for i,jet in enumerate(genJets):
        ##     print ' %5d: %6.2f %6.2f %6.2f %6.2f' % (i, jet.pt, jet.eta, jet.phi, jet.mass)
        print '-------'            
        print "On-the-fly Gen jets:"
        for i,sdjet in enumerate(sdjets):
            print ' %5d: %6.2f %6.2f %6.2f %6.2f' % (i, sdjet.perp(), sdjet.eta(), sdjet.phi(), sdjet.m())
            print 'Subjets:'
            subs = sdjet.pieces()
            for j,sub in enumerate(subs):
                print '      : %6.2f %6.2f %6.2f %6.2f' % (sub.perp(), sub.eta(), sub.phi(), sub.m())
        print '-------'

            
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

sdb0 = lambda : softDropProducer(beta=0.0, zcut=0.1, bname="sdb0")
sdb1 = lambda : softDropProducer(beta=1.0, zcut=0.1, bname="sdb1")
