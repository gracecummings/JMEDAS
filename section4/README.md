# Jet types at the LHC

Jets are reconstructed physics objects representing the hadronization and fragmentation of quarks and gluons. CMS mostly uses anti-$k_{\mathrm{T}}$ jets with a cone-size of $R=0.4$ to reconstruct this type of jet. We have algorithms that distinguish heavy-flavour (b or c) quarks (which are in the domain of the BTV POG), quark- vs gluon-originated jets, and jets from the main $pp$ collision versus jets formed largely from pileup particles. 

However, quarks and gluons are only part of the story! At the LHC, the typical collision energy is much greater than the mass scale of the known SM particles, and hence even heavier particles like top quarks, W/Z/Higgs bosons, and heavy beyond-the-Standard-Model particles can be produced with large Lorentz boosts. When these particles decay to quarks and gluons, their decay products are collimated and overlap in the detector, making them difficult to reconstruct as individual AK4 jets. 

Therefore, LHC analyses use jet algorithms with a large radius parameter to reconstruct these objects, which we called "large radius" or "fat" jets. CMS uses anti-$k_{\mathrm{T}}$ jets with $R=0.8$ (AK8) as the standard large-radius jet, while ATLAS uses AK10. 

This topic was explained in more detailed in the slides [ADD LINK TO SLIDES]. You can also read these excellent overviews of jet substructure techniques:

- [Boosted objects: a probe of beyond the Standard Model physics](http://arxiv.org/abs/1012.5412) by Abdesselam et al.
- [Looking inside jets: an introduction to jet substructure and boosted-object phenomenology](https://arxiv.org/abs/1901.10342) by Marzani, Soyez, and Spannowsky.

## Jet types and algorithms in CMS

The standard jet algorithms are all implemented in the CMS reconstruction software, [CMSSW](github.com/cms-sw/cmssw). However, a few algorithms with specific parameters (namely AK4, AK8, and CA15) have become standard tools in CMS; these jet types are extensively studied by the JetMET POG, and are highly recommended. These algorithms are included in the centrally produced CMS samples, at the AOD, miniAOD, and nanoAOD data tiers (note that miniAOD and nanoAOD are most commonly used for analysis, while AOD is much less common these days, and is not widely available on the grid). Other algorithms can be implemented and tested using the **JetToolbox** (discussed later in the tutorial).  

In this part of the tutorial, you will learn how to access the jet collection included in the CMS datasets, do some comparisons of the different jet types, and how to create your own collections. 


### AOD 

[This twiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideDataFormatRecoJets) summarizes the respective labels by which each jet collection can be retrieved from the event record for general AOD files. This format is currently been used for specialized studies, but for most of the analyses you can use the other formats.

### MiniAOD

There are three main jet collections for Run 2 stored in the MiniAOD format, as described [here](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2017#Jets).
 * **slimmedJets**: are AK4 energy-corrected jets using charged hadron substraction (CHS) as the pileup removal algorithm. This is the default jet collection for CMS analyses for Run II. In this collection you can find the following jet algorithms, as well as other jet related quantities:
   * b-tagging 
   * Pileup jet ID
   * Quark/gluon likelihood info embedded.
 * **slimmedJetsPUPPI**: are AK4 energy-corrected jets using the PUPPI algorithm for pileup removal. This collection will be the default for Run III analyses.
 * **slimmedJetsAK8**: ak4 AK8 energy-corrected jets using the PUPPI algoritm for pileup removal. This has been the default collection for boosted jets in Run II. In this collection you can find the following jet algorithms, as well as other jet related quantities:
   * Softdrop mass
   * n-subjettiness and energy correlation variables
   * Access to softdrop subjets
   * Access to the associated AK8 CHS jet four momentum, including softdrop and pruned mass, and n-subjettiness.

### Examples of how to access jet collections in miniAOD samples

Below are two examples of how to access jet collections from these samples. This exercise does not intend for you to modify code in order to access these collections, but rather for you to look at the code and get an idea about how you could access this information if needed.

##### In C++

Please take a look at the file `$CMSSW_BASE/src/Analysis/JMEDAS/src/jmedas_miniAODAnalyzer.C` with your favourite code viewer.

You can run this code by using the python config file `$CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_miniAODtest.py` from your terminal. This script will only print out some information about the jets in that sample. Again, the most important part of this exercise is to get familiar with how to access jet collections from miniAOD. Take a good look at the prints this script produces to your terminal.

```
cmsRun $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_miniAODtest.py
```

##### In Python

Now take a look at the file `$CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_miniAODtest_purePython.py`.

This code can be run with simple python in your terminal. Similar as in the case for C++, the output of this job is some information about jets. The most important part of the exercise is to get familiar with how to access jet collections using python from miniAOD.

To run:

```
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_miniAODtest_purePython.py
```

### NanoAOD

In nanoAOD, only AK4 CHS jets ( _Jet_ ) and AK8 PUPPI jets ( _FatJet_ ) are stored. The jets in nanoAOD are similar to those in miniAOD, but not identical (for example, the $p_{\mathrm{T}}$ cuts might be different). A full set of variables for each jet collection can be found in this [website](https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html).

NanoAOD is a "flat tree" format, meaning that you can access the information directly with simple ROOT, or even simple python tools (like numpy or pandas). This format is becoming more and more popular within CMS due to its simplicity and accesibility. Open `$CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_nanoAODtest.py`) in your favorite text editor to see what it looks like, if you are interested. Try running this now in your cmslpc session with python.

```
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_nanoAODtest.py
```

*Aside*: there are several more advanced tools on the market which allow you to do more sophisticated analysis using nanoAOD format, including [RDataFrame](https://root.cern/doc/master/classROOT_1_1RDataFrame.html), [NanoAOD-tools](https://github.com/cms-nanoAOD/nanoAOD-tools), or [Coffea](https://github.com/CoffeaTeam/coffea). We excourage you to look at them and use the one you like the most.

### JetToolBox

Although JME generally recommends to use AK4 CHS and AK8 PUPPI jets for Run II analyses (moving fully to AK4 PUPPI jets for Run III), there are cases where certain analysis will need to use something else. Similar for the standard algorithms stored in mini/nanoAOD samples. For users who want to test a different jet collection or algorithms, JetMET had developed a user-friendly tool to compute them: [JetToolbox](https://twiki.cern.ch/twiki/bin/view/CMS/JetToolbox).

The JetToolbox is *not* part of CMSSW because JME wants to have the freedom to incorporate and test as many tools as possible without these algorithms being part of any central samples or code. That is the reason that, in real life, you would need to clone the [JetToolbox repository](https://github.com/cms-jet/JetToolbox) inside your CMSSW src folder like this:

```
cd $CMSSW_BASE/src/
git clone git@github.com:cms-jet/JetToolbox.git JMEAnalysis/JetToolbox -b jetToolbox_102X_v3
scram b
```

In this tutorial, this step was done for you in the initial setup. _You do not need to do it now_. You can find more information about how to set up the JetToolbox in the [README.md](https://github.com/cms-jet/JetToolbox) of the github repository or in the [twiki](https://twiki.cern.ch/twiki/bin/view/CMS/JetToolbox).

