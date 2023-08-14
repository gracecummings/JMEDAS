# Reminder of what we are doing

The tutorial is designed to be executed at cmslpc and followed along with the second day of the Jets HATs [Indico page](https://indico.cern.ch/event/1311545/)

go to `section3` in the `JMEDAS` directory to begin the exercise.

# Jet Energy Corrections

From the previous exercise, recall the comparison of PFJets with GenJets. Let's plot a reco-jet vs gen-jet comparison again for a refresher with the below script 'JEC_part1.py' and open the produced JEC_part1.pdf.

The $p_{\mathrm{T}}$ distributions disagree quite a bit between the GenJets and PFJets. We need to apply the *jet energy corrections* (JECs), a sequence of corrections that address non-uniform responses in $p_{\mathrm{T}}$ and $\eta$, as well as an average correction for pileup. The JECs are often updated fairly late in the analysis cycle, simply due to the fact that the JEC experts start deriving the JECs at the same time the analyzers start developing their analyses. For this reason, it is imperative for analyzers to maintain flexibility in the JEC, and the software reflects this. It is possible to run the JEC software "on the fly" after you've done your heavy processing (PAT-tuple creation, skimming,etc). We will now show how this is done.

For more information and technical details on the jet energy scale calibration in CMS, look at the following twiki: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections. 

Start by running the histogram-making code, this time asking it to apply the JECs. While it's running, take a look at the code and make sure you understand the parts relevant to JEC (try a text search for "args.correctJets"). 

```
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_make_histograms.py --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/ttjets2023.txt --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/ttjets_corr.root --maxevents=2000 --maxjets=6 --maxFiles 10 --correctJets Fall17_17Nov2017_V32_MC
```

The string "Fall17_17Nov2017_V32" points to the JEC text files in the directory /data/JECs, which were downloaded from [this twiki](https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC). You can also create the text files using the JetCorrectorDBReader module in CMSSW (see the cmsRun cfg at scripts/JetCorrectionDBReader_cfg.py), but for technical reasons, this method can be error-prone (see the JEC twiki for more details). 

## Exercise: Before and after JECs

Let's check the GenJets-PFJets agreement after applying the JECs with the `JEC_part2.py` script.

Have a look at the script, execute it and open the produced two plots. Inspect the plots carefully to see the differences between corrected, uncorrected and generator-level jets.

## JEC Uncertainties

Since we've applied the JEC corrections to the distributions, we should also assign a systematic uncertainty to the procedure. The procedure is explained at [this twiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#JetCorUncertainties). 

The uncertainties are implemented in `jmedas_make_histograms.py`. The histogram files you've made already have the up- and down-variation histograms. The relevant piece of code is:

```
corr = 1.0
corrUp = 1.0
corrDn = 1.0
# Get the latest, greatest jet corrections
if args.correctJets : 
    jec.setJetEta( uncorrJet.eta() )
    jec.setJetPt ( uncorrJet.pt() )
    jec.setJetE  ( uncorrJet.energy() )
    jec.setJetA  ( jet.jetArea() )
    jec.setRho   ( rhoValue[0] )
    jec.setNPV   ( len(pvs) )
    icorr = jec.getCorrection()
    corr *= icorr
    corrUp *= icorr
    corrDn *= icorr


    #JEC Uncertainty
    jecUnc.setJetEta( uncorrJet.eta() )
    jecUnc.setJetPhi( uncorrJet.phi() )
    jecUnc.setJetPt( corr * uncorrJet.pt() )
    corrUp += jecUnc.getUncertainty(1)
    jecUnc.setJetEta( uncorrJet.eta() )
    jecUnc.setJetPhi( uncorrJet.phi() )
    jecUnc.setJetPt( corr * uncorrJet.pt() )
    corrDn -= jecUnc.getUncertainty(0)


h_ptAK4.Fill( corr * uncorrJet.pt() )
h_JECValueAK4.Fill( corr )
h_ptUncorrAK4.Fill( uncorrJet.pt() )
h_ptDownAK4.Fill( corrDn * uncorrJet.pt() )
h_ptUpAK4.Fill( corrUp * uncorrJet.pt() )
```

Now run the script `JEC_uncertainty.py` to plot a comparison of the nominal and varied jet energy spectra. Does the result make sense? Is the nominal histogram always between the up and down variations, and should it be?

## Discussion
Why do we need to calibrate jet energy? Why is "jet response" not equal to 1? Can you think of a physics process in nature that can help us calibrate the jet response to 1?

The amount of material in front of the CMS calorimeter varies by $\eta$. Therefore, the calorimeter response to jet is also a function of jet $\eta$. Can you think of a physics process in nature that can help us calibrate the jet response in $\eta$ to be uniform?