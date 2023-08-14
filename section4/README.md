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
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_make_histograms.py --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/rsgluon_ttbar_3000GeV.txt --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/rsgluon_ttbar_3000GeV.root --maxevents=2000 --maxFiles 1 --maxjets=6
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_make_histograms.py --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/ttjets.txt --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/ttjets.root --maxevents=2000 --maxjets=6 --maxFiles 5
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_make_histograms.py --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/WJetsToQQ_HT600to800.txt --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/WJetsToQQ_HT600to800.root --maxevents=2000 --maxjets=4 --maxFiles 2 --matchPdgIdAK8 24 0.8    
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_make_histograms.py --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/QCD_Pt_470to600.txt --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/QCD_Pt_470to600.root --maxevents=2000 --maxjets=4 --maxFiles 2
```

## Grooming and PU removal algorithms

Now, let's compare the jet masses for ungroomed, pruned, soft drop (SD), PUPPI, and SD+PUPPI.

```
cd section4
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