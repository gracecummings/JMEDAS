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

# Jet Substructure

Because boosted jets represent the hadronic products of a heavy particle produced with high momentum, some tools have been developed to study the internal structure of these jets. This topic is usually called Jet Substructure. 

Jet substructure algorithms can be divided into three main tools:
 * **grooming algorithms** attempt to reduce the impact of *soft* contributions to clustering sequence by adding some other criteria. Examples of these algorimths are softdrop, trimming, pruning.
 * **subtructure variables** are observables that try to quantify how many cores or prongs can be identify within the structure of the boosted jet. Examples of these variables are n-subjetiness or energy correlation functions.
 * **taggers** are more sofisticated algorithms that attempt to identify the origin of the boosted jet. Currently taggers are based on sofisticated machine-learning techniques which try to use as much information as possible in order to efficiency identify boosted W/Z/Higgs/top jets. Examples of these taggers in CMS are deepAK8/ParticleNet or deepDoubleB.
 
For further reading, several measurements have been performed about jet substructure:
 * [Studies of jet mass in dijet and W/Z+jet events](http://arxiv.org/abs/1303.4811) (CMS).
 * [Jet mass and substructure of inclusive jets in sqrt(s) = 7 TeV pp collisions with the ATLAS experiment](http://arxiv.org/abs/1203.4606) (ATLAS).
 * [Theory slides](http://www.hri.res.in/~sangam/sangam18/talks/Marzani-2.pdf) 
 * [More theory slides]( http://indico.hep.manchester.ac.uk/getFile.py/access?contribId=14&resId=0&materialId=slides&confId=4413)
 * [Talk from Phil Harris](https://web.pa.msu.edu/seminars/hep_seminars/abstracts/2018/Harris-HEPSeminar-Slides-4172018.pdf) on searching for boosted $W$ bosons.
 
In this part of the tutorial, we will compare different subtructure algorithms as well as some usually subtructure variables.

The code we will use `$CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_make_histograms.py` is a python-based script accessing miniAOD information. We used it in the previous exercise.

The code will take several minutes to run, so you can launch the script first, and read the script while the code is running. To run, execute the following:

```
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_make_histograms.py 
    --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/rsgluon_ttbar_3000GeV.txt 
    --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/rsgluon_ttbar_3000GeV.root 
    --maxevents=2000 
    --maxFiles 1 
    --maxjets=6
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_make_histograms.py 
    --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/ttjets.txt 
    --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/ttjets.root 
    --maxevents=2000 
    --maxjets=6 
    --maxFiles 5
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_make_histograms.py 
    --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/WJetsToQQ_HT600to800.txt 
    --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/WJetsToQQ_HT600to800.root 
    --maxevents=2000 
    --maxjets=4 
    --maxFiles 2 
    --matchPdgIdAK8 24 0.8    
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_make_histograms.py 
    --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/QCD_Pt_470to600.txt 
    --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/QCD_Pt_470to600.root 
    --maxevents=2000 
    --maxjets=4 
    --maxFiles 2
```

## Grooming and PU removal algorithms

Now, let's compare the jet masses for ungroomed, pruned, soft drop (SD), PUPPI, and SD+PUPPI.

```
python jet_substructure_part1.py
evince jet_substructure_part1.pdf
```

The histogram should look roughly like this (but with added normalization):

![jet grooming algo comparisons](../notebooks/files/ex5_rsg_jetmass.png)

Note that the histogram has two peaks, what do these correspond to? How do the algorithms affect the relative size of the two populations?

# Substructure Variables

Now, let's compare the different subtructure variables between two different samples. Using the histograms that you created in the previous steps, the next script contains just a function to create comparison plots.

Let's start with n-subjetiness ratios. The variable $\tau_N$ gives a sense of how many N prongs or cores can be find inside the jet. It is known that the n-subjetiness variables itself ($\tau_{N}$) do not provide good discrimination power, but its ratios do. Then, a $\tau_{MN} = \dfrac{\tau_M}{\tau_N}$ basically tests if the jet is more M-prong compared to N-prong. For instance, we expect 2 prongs for boosted jets originated from hadronic Ws, while we expect 1 prongs for high-pt jets from QCD multijet processes.

Let's compare one of the most common nsubjetiness ratio $\tau_{21}$. Run `compare_histograms.py` and open the resulting pdf:

```
python compare_histograms.py
evince 
```

What can you say about the two histograms? Is $\tau_{21}$ telling you something about the nature of the boosted jets selected?

Let's compare now $\tau_{32}$. Modify the function call `compareHistogram('tau21AK8', processes=["rsg", "wqq", "qcd"])` in the script and produce plots with the two following configurations:

```
compareHistogram('tau32AK8', processes=["rsg", "qcd"])
compareHistogram('tau32AK8_pt450', processes=["rsg", "qcd"])
```

What can you say about the two histograms? Is $\tau_{32}$ telling you something about the nature of the boosted jets selected?

Another substructure variable commonly used is the energy correlation function $N2$. Similarly than $\tau_{21}$, $N2$ tests if the boosted jet is compatible with a 2-prong jet hypothesis. Let's compare now $N2$ and $N3$. Follow the above process with these:

```
compareHistogram( 'ak8_N2_beta1', processes=["rsg", "wqq", "qcd"] )
compareHistogram( 'ak8_N3_beta1_pt450', processes=["rsg", "qcd"] )
```

What can you say about the two histograms? Are $N2$ and $N3$ telling you something about the nature of the boosted jets selected?

# $\rho$ parameter
A useful variable for massive, fat jets is the QCD scaling parameter $\rho$, defined as:

$\rho=\log(m^2/(p_{\mathrm{T}}R)^2)$.

(Sometimes $\rho$ is defined without the log). One useful feature of this variable is that QCD jet mass grows with $p_{\mathrm{T}}$, i.e. the two quantities are strongly correlated, while $\rho$ is much less correlated with $p_{\mathrm{T}}$.
Repeat the above plotting process with these two function calls and open the plots:

```
compareHistogram( 'logrhoRatioAK8' )
compareHistogram( 'rhoRatioAK8' )
```
The following two plots show what QCD events look like in different $p_{T}$ ranges. It's clear that the mass depends very strongly on $p_{T}$, while the $\rho$ shape is fairly constant vs. $p_{T}$ (ignoring $\rho<7$ or so, which is the non-perturbative region). Having a stable shape is useful when studying QCD across a wide $p_{T}$ range.

![qcd pt mass](../notebooks/files/qcdpt_mass.png)
![qcd pt rho](../notebooks/files/qcdpt_rho.png)

# W and top tagging

In this part of the tutorial, we will look at how different substructure algorithms can be used to identify jets originating from boosted W's and tops. Specifically, we'll see how these identification tools are used to separate these boosted jets from those originating from Standard Model QCD, a dominant process at the LHC.

Run the following commands to produce the relevant histogram files from the SM ttbar, RS KK gluon, and QCD samples. It may take a few minutes - go ahead a grab a coffee while it runs.

```
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_make_histograms.py --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/ttjets.txt --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/ttjets.root --maxevents=2000 --maxFiles 10 --maxjets=6
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_make_histograms.py --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/rsgluon_ttbar_3000GeV.txt --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/rsgluon_ttbar_3TeV.root --maxevents=2000 --maxFiles 10 --maxjets=6
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_make_histograms.py --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/QCD_Pt_300to470.txt --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/QCD_Pt_300to470.root --maxevents=2000 --maxFiles 10 --maxjets=6
```

## W Tagging

We will now investigate how to identify W bosons using the substructure techniques we've learned. 

Compare the tau2 / tau1 ratio for the AK8 jets from Standard Model top quarks to those from the QCD sample using the below script `W_tagging_part1.py.

```
python W_tagging_part1.py
```

Now compare with the energy correlation function, N2b1, with `W_tagging_part2.py:

```
python  W_tagging_part2.py
```

### Quiz

* Why can we use a ttbar sample to talk about W-tagging? (Hint: look at the two peaks in the jet mass plots later in the exercise.)
* What cuts would you place on these variables to distinguish W bosons from QCD?
* So far, which variable looks more promising?

# Top Tagging

We will now investigate how to identify top quarks using the substructure techniques we've learned.

Compare the tau3/ tau2 ratio for the boosted top quarks from the RS KK gluon sample, and the jets from the QCD sample using the `T_tagging_part1.py script.

```
python T_tagging_part1.py
```

### Quiz

* What cut would you apply to select boosted top quarks?
* For both the W and top selections, what other variable(s) could we cut on in addition?

# Jet Mass

We can also use jet mass to distinguish our boosted W and top jets from QCD. Let's compare the AK8 jet mass of the boosted top quarks from the RS KK sample and the jets from the QCD sample. Let's also look at the ungroomed jet mass (labeled as CHS) and the softdrop groomed jet mass combined with the PUPPI pileup subtraction algorithm.
Execute the following `jet_mass.py script in terminal and open the plot.

```
python jet_mass.py
evince 
```

# Quiz

* Which does better at separating the QCD from both the top and W mass peaks - CHS or softdrop + PUPPI?

# Go Further

* You can learn more about PUPPI from the pileup mitigation exercise.
* We briefly mentioned that you can combine variables for even better discrimination. In CMS, we do this to build some of our jet taggers. For the simple taggers, we often combine cuts on jet substructure variables and jet mass. The more sophisticated taggers, which are used more and more widely within CMS, use deep neural networks. To learn about building a machine learning tagger, check out the [machine learning short exercise](https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideCMSDataAnalysisSchoolCERN2020MLShortExercise)