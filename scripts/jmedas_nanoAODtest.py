# import ROOT in batch mode
import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
from ROOT import *
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv

inputFile = TFile.Open('root://xrootd-cms.infn.it//store/mc/RunIISummer20UL18NanoAODv9/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/60000/A7D190CE-A78E-B14B-80E0-0565DF0D87BA.root' )
events = inputFile.Get('Events')

for iev in xrange(events.GetEntries()):
    events.GetEntry(iev)
    if iev >= 10: break

    print "\nEvent %d: run %6d, lumi %4d, event %12d" % (iev, events.run, events.luminosityBlock, events.event )

    # AK4 CHS Jets
    for ijet in range(events.nJet):
        if events.Jet_pt < 20: continue
        print 'AK4 jet '+ str(ijet) + ': pt ' + str(events.Jet_pt[ijet]) + ', eta ' + str(events.Jet_eta[ijet]) + ', mass ' + str(events.Jet_mass[ijet]) + ',phi ' + str(events.Jet_phi[ijet]) + ', puId ' + str(events.Jet_puId[ijet]) + ', deepJet btag disc. ' + str(events.Jet_btagDeepB[ijet])

    # AK8 PUPPI Jets
    for ijet in range(events.nFatJet):
        if events.FatJet_pt < 20: continue
        print 'AK8 jet '+ str(ijet) + ': pt ' + str(events.FatJet_pt[ijet]) + ', eta ' + str(events.FatJet_eta[ijet]) + ', mass ' + str(events.FatJet_mass[ijet]) + ',phi ' + str(events.FatJet_phi[ijet]) + ', deepAK8 W tag disc. ' + str(events.FatJet_deepTag_WvsQCD[ijet])+ ', deepAK8 top tag disc. ' + str(events.FatJet_deepTag_TvsQCD[ijet])
