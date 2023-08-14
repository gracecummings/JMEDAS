# Jet Types and Algorithms

## Jet Basics

This preliminary exercise will illustrate some of the basic properties of jets in CMS. Let's start by running the histogram-making code on some $t\bar{t}$ MC. While the script is running, take a look at the script and make sure you understand what it's doing.

```
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_make_histograms.py --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/ttjets2023.txt --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/ttjets.root --maxevents=2000 --maxjets=6 --maxFiles 2
```

Now let's plot the resulting histograms. Take a look at the simple plotting script below and execute it with

```
cd section1
python basics.py
```
You can open the produced pdf file with evince:

```
evince plots1.pdf&
```

Your histograms from the script should look similar to the four plots shown below. What about AK8 jets? Add the corresponding histograms to the same canvases, they are already filled and available (draw option 'same', line color 'ROOT.kRed').
Open basics.py with a code editor, such as gedit, emacs, nano or vim, add the needed lines for AK8 and reproduce the plots.

![Basic jet kinematics](../notebooks/files/plots1.png)

## Jet Types

The jet algorithms take as input a set of 4-vectors. At CMS, the most popular jet type is the "Particle Flow Jet", which attempts to use the entire detector at once and derive single four-vectors representing specific particles.For this reason it is very comparable (ideally) to clustering generator-level four-vectors also.

### Particle Flow Jets (PFJets)

Particle Flow candidates (PFCandidates) combine information from various detectors to make a combined estimation of particle properties based on their assigned identities (photon, electron, muon, charged hadron, neutral hadron).

PFJets are created by clustering PFCandidates into jets, and contain information about contributions of every particle class: Electromagnetic/hadronic, Charged/neutral etc.

The jet response is high. The jet pT resolution is good: starting at 15--20% at low pT and asymptotically reaching 5% at high pT.

### Monte Carlo Generator-level Jets (GenJets)

GenJets are pure Monte Carlo simulated jets. They are useful for analysis with MC samples. GenJets are formed by clustering the four-momenta of Monte Carlo truth particles. This may  particles (muons, neutrinos, WIMPs, etc.).

As there are no detector effects involved, the jet response (or jet energy scale) is 1, and the jet resolution is perfect, by definition.

GenJets include information about the 4-vectors of the constituent particles, the hadronic and electromagnetic components of the energy etc.

### Calorimeter Jets (CaloJets)

CaloJets are formed from energy deposits in the calorimeters (hadronic and electromagnetic), with no tracking information considered. In the barrel region, a calorimeter tower consists of a single HCAL cell and the associated 5x5 array of ECAL crystals (the HCAL-ECAL association is similar but more complicated in the endcap region). The four-momentum of a tower is assigned from the energy of the tower, assuming zero mass, with the direction corresponding to the tower position from the interaction point.

In CMS, CaloJets are used less often than PFJets. Examples of their use include performance studies to disentangle tracker and calorimeter effects, and trigger-level analyses where the tracker is neglected to reduce the event processing time. ATLAS makes much more use of CaloJets, as their version of particle flow is not as mature as CMS's.invisibleinclude 

### Exercise: Reconstructed vs. Generator-Level Jets

Execute the following script to make some more jet histograms, this time from QCD MC. 

```
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_make_histograms.py --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/QCD_Pt_470to600.txt --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/qcd_470to600.root --maxevents=10000 --maxFiles 5 --maxjets=2
python jet_types_and_algorithms.py
```

Open the produced plot with `evince jet_types_and_algorithms.pdf&`. As you can see, the agreement isn't very good! Can you guess why?

## Jet Clustering Algorithms

The majority of jet algorithms at CMS use a so-called "clustering sequence". This is essentially a pairwise examination of the input four-vectors. If the pair satisfy some criteria, they are merged. The process is repeated until the entire list of constituents is exhausted. In addition, there are several ways to determine the "area" of the jet over which the input constituents lay. This is very important in correcting for pileup, as we will see, because some algorithms tend to "consume" more constituents than others and hence are more susceptible to pileup. Furthermore, the amount of energy that is inside of a jet due to pileup is proportional to the area, so to correct for this effect it is very important to know the jet area.

![Four different clustering algorithm comparison](../notebooks/files/JHEP04_2008_063.jpg)

Figure: Comparison of jet areas for four different jet algorithms, from "The anti-kt Clustering Algorithm" by Cacciari, Salam, and Soyez [JHEP04, 063 (2008), arXiv:0802.1189].

Some excellent references about jet algorithms can be found here:

- [Toward Jetography](http://arxiv.org/abs/0906.1833) by Gavin Salam.
- [Jets in Hadron-Hadron Collisions](http://arxiv.org/abs/0712.2447) by Ellis, Huston, Hatakeyama, Loch, and Toennesmann
- [The Catchment Area of Jets](http://arxiv.org/abs/0802.1188) by Cacciari, Salam, and Soyez.
- [The anti-kt Clustering Algorithm](http://arxiv.org/abs/0802.1189) by Cacciari, Salam, and Soyez.

### Exercise: Comparing jet areas between AK4 and AK8

Run `python jet_cone_sizes.py` to plot a comparison of the jets areas between AK4 and AK8 jets. A priori, what type of distribution do you expect?

Try modifying the plotting script to add vertical lines at area values corresponding to $\pi R^2$. Do the histogram peaks line up with these values?

<details>
<summary>
    <font color='blue'>Show answer...</font>
</summary>

The histograms indeed peak at the expected value of $\pi R^2$. 
```
line_ak4 = ROOT.TLine(math.pi * 0.4**2, 0., math.pi * 0.4**2, frame.GetMaximum())
line_ak4.SetLineWidth(2)
line_ak4.SetLineStyle(2)
line_ak4.SetLineColor(ROOT.kGray)
line_ak4.Draw()

line_ak8 = ROOT.TLine(math.pi * 0.8**2, 0., math.pi * 0.8**2, frame.GetMaximum())
line_ak8.SetLineWidth(2)
line_ak8.SetLineStyle(2)
line_ak8.SetLineColor(ROOT.kGray)
line_ak8.Draw()
```
</details>

## Jet ID

in order to avoid using fake jets, which can originate from a hot calorimeter cell or electronic read-out box, we need to require some basic quality criteria for jets. These criteria are collectively called "jet ID". Details on the jet ID for PFJets can be found in the following twiki:

[https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID](https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID)

The JetMET POG recommends a single jet ID for most physics analysess in CMS, which corresponds to what used to be called the tight Jet ID. Some important observations from the above twiki:

- Jet ID is defined for uncorrected jets only. Never apply jet ID on corrected jets. This means that in your analysis you should apply jet ID first, and then apply JECs on those jets that pass jet ID.
- Jet ID is fully efficient (>99%) for real, high-$p_{\mathrm{T}}$ jets used in most physics analysis. Its background rejection power is similarly high.

### Applying Jet ID

There are several ways to apply jet ID. In our above exercises, we have run the cuts "on-the-fly" in our python FWLite macro. The Jet ID can be applied as a series of cuts. The following examples use somewhat out of date numbers. See the above link to the JetID twiki for the current numbers. To apply the cuts on pat::Jet (like in miniAOD) in python then you can do:

<details>
<summary>
    <font color='blue'>Show...</font>
</summary>

```
# Apply jet ID to uncorrected jet
nhf = jet.neutralHadronEnergy() / uncorrJet.E()
nef = jet.neutralEmEnergy() / uncorrJet.E()
chf = jet.chargedHadronEnergy() / uncorrJet.E()
cef = jet.chargedEmEnergy() / uncorrJet.E()
nconstituents = jet.numberOfDaughters()
nch = jet.chargedMultiplicity()
goodJet = 
  nhf < 0.99 && 
  nef < 0.99 && 
  chf > 0.00 && 
  cef < 0.99 && 
  nconstituents > 1 && 
  nch > 0
```
</details>

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