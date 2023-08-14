import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10)  )

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
                                        '/store/mc/RunIISummer20UL18MiniAODv2/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/50000/60FABBC4-D5AD-2142-9BC4-03C1D7DB6D7F.root'

                            )
                            )

process.demo = cms.EDAnalyzer("MiniAnalyzer",
                                  vertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
                                  jets = cms.InputTag("slimmedJets"),
                                  fatjets = cms.InputTag("slimmedJetsAK8")
                              )

process.p = cms.Path(process.demo)
