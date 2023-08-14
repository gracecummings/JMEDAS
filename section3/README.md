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

# Jet Energy Resolution

Jets are stochastic objects. The content of jets fluctuates quite a lot, and the content also depends on what actually caused the jet (uds quarks, gluons, etc). In addition, there are experimental limitations to the measurement of jets. Both of these aspects limit the accuracy to which we can measure the 4-momentum of a jet. The way to quantify our accuracy of measuring jet energy is called the jet energy resolution (JER). If you have a group of single pions that have the same energy, the energy measured by CMS will not be exactly the same every time, but will typically follow a (roughly) Gaussian distribution with a mean and a width. The mean is corrected using the jet energy corrections. It is impossible to "correct" for all resolution effects on a jet-by-jet basis, although regression techniques can account for many effects.

As such, there will always be some experimental and theoretical uncertainty in the jet energy measurement, and this is seen as non-zero jet energy resolution. There is also other jet-related resolutions such as jet angular resolution and jet mass resolution, but JER is what we most often have to deal with.
Jets measured from data have typically worse resolution than simulated jets. Because of this, it is important to 'smear' the MC jets with jet energy resolution (JER) scale factors, so that measured and simulated jets are on equal footing in analyses. We will demonstrate how to apply the JER scale factors, since that is applicable for all analyses that use jets. More information can be found at the jet resolution twiki and jet resolution software guide. The resolution is measured in data for different eta bins, and was approximately 10% with a 10% uncertainty for 7 TeV and 8 TeV data. For precision, it is important to use the correctly measured resolutions, but a reasonable calculation is to assume a flat 10% uncertainty for simplicity.

To perform this on `pat::Jets` in MC miniAOD, the syntax is:

```
smear = getJER(jet.eta(), 0) #JER nominal=0, up=+1, down=-1
smearUp = getJER(jet.eta(), 1) #JER nominal=0, up=+1, down=-1
smearDn = getJER(jet.eta(), -1) #JER nominal=0, up=+1, down=-1
recopt = jet.pt()
genpt = genJet.pt()
deltapt = (recopt-genpt)*(smear-1.0)
deltaptUp = (recopt-genpt)*(smearUp-1.0)
deltaptDn = (recopt-genpt)*(smearDn-1.0)
ptsmear = max(0.0, (recopt+deltapt)/recopt)
ptsmearUp = max(0.0, (recopt+deltaptUp)/recopt)
ptsmearDn = max(0.0, (recopt+deltaptDn)/recopt)
corr *= ptsmear
corrUp *= ptsmearUp
corrDn *= ptsmearDn
```

You can see that the smearing scales the difference between the reconstructed and truth-level jet $p_{\mathrm{T}}$s. The smearing value is taken from the function `getJER()`. 

Run the below command in cmslpc to create histograms with the JER smearing applied. As usual, open `jmedas_make_histograms.py` again, and understand what the `getJER()` function does.  

```
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_make_histograms.py --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/ttjets2023.txt --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/ttjets_corr_smear.root --maxevents=2000 --maxFiles 10 --maxjets=2 --correctJets Fall17_17Nov2017_V32_MC --smearJets
```

Next, let's make plots of the output with

```
python JER_part1.py
```

and then open the resulting pdf. In our example, which has a larger effect: jet energy correction uncertainty, or jet energy resolution uncertainty?

## Dijet resonance peaks
As a final exercise for the first part of this exercise, let's look at a simple dijet resonance peak. The following cell will produce histograms from an MC sample of Randall-Sundrum gravitons (RSGs) with m=3 TeV decaying to two quarks. The resulting signature is two high-$p_{\mathrm{T}}$ jets, with a truth-level invariant mass of 3 TeV. 

Execute the below commands in terminal and while the code is running, look at the script (scripts/jmedas_dijet.py). Hint: you can execute all the processes at once by copy-pasteing all rows from the below script box at once. Be patient, this takes a while.

```
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_dijet.py --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/rsgluon_qq_3000GeV.txt --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/rsgluon_qq_3000GeV.root --maxevents=4000 --maxjets=6
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_dijet.py --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/rsgluon_qq_3000GeV.txt --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/rsgluon_qq_3000GeV_corr.root --maxevents=4000 --maxjets=6 --correctJets Fall17_17Nov2017_V32_MC
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_dijet.py --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/rsgluon_qq_3000GeV.txt --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/rsgluon_qq_3000GeV_smear.root --maxevents=4000 --maxjets=6 --smearJets
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_dijet.py --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/rsgluon_qq_3000GeV.txt --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/rsgluon_qq_3000GeV_corr_smear.root --maxevents=4000 --maxjets=6 --correctJets Fall17_17Nov2017_V32_MC --smearJets
```

When the above running is done, plot the output with

```
python JER_part2.py
```