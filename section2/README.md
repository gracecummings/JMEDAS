# Reminder of setup

The tutorial is designed to be executed at cmslpc and followed along with the second day of the Jets HATs [Indico page](https://indico.cern.ch/event/1311545/)

## Run exercises in cmslpc

Open a terminal/console, connect to cmslpc-sl7 and prepare your working area (instructions are in bash shell syntax):

```
kinit username@FNAL.GOV
ssh -Y username@cmslpc-sl7.fnal.gov
mkdir JMEHATS2023
cd JMEHATS2023

export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsrel CMSSW_10_6_18
cd CMSSW_10_6_18/src
cmsenv
```

In some exercises we also need to access files in remote servers, so activate your grid certificate:
```
voms-proxy-init -voms cms -valid 192:00
```

## Get the newest version of the code

```
cd Analysis/JMEDAS
```

Remember to check that you are on the `HATS2023` branch, and if you are not, switch to it. Do a `git pull`

```
git status
git checkout HATS2023
git pull
```

The pull probably will not work because you have accummualted changes during the first day of the tutorial. If you want to keep these changes, make a new branch, and commit them there. Otherwise, just use `git stash`.

```
git stash
git pull
```

Now you should have the most up-to-date version of the repository. These exercises will be in `section2` of the repo, so navigate there

```
cd section2
```

# Measuring pileup

Before we get into mitigating pileup effects, let's first examine measures of pileup in more detail. We will discuss event-by-event variables that can be used to characterize the pileup and this will give us some hints into thinking about how to deal with it.

If you are familiar with the ROOT command line (clang) then all of the quantities we want to look at can be computed interactively. However, to move things along we have provided a set of python commands which will display the necessary information. Take a look at the pileup.py script below before executing it and opening the produced plot with evince.

```
python pileup.py
evince pileup.pdf&
```

Question 1: Why are there a different amount of pileup interactions than primary vertices?

<details>
<summary>Show answer...</summary>
There is a vertex finding efficiency, which in Run I was about 72%. This means that $N_{PV}\simeq0.72{\cdot}N_{PU}$
</details>

Question 2: How many pileup interactions are simulated before and after the in-time bunch crossing?

<details>
<summary>Hint</summary>
Open the file on the ROOT command line, and scan the tree with 

```
t.Scan("bxns:tnpu:npu")
````
</details>

<details>
<summary>Show answer...</summary>
There are 12 interactions before and 3 after.
</details>

Question 3: Rho is the measure of the density of the pileup in the event. It's measured in terms of GeV per unit area. Can you think of ways we can use this information the correct for the effects of pileup?

<details>
<summary>Show answer...</summary>
From the jet $p_{T}$ simply subtract off the average amount of pileup expected in a jet of that size. Thus $p_{T}^{corr}{\simeq}p_{T}^{reco}-\rho{\cdot}area$
</details>

Question 4: This plot shows the jet composition. Generally, why do we see the mixture of photons, neutral hadrons and charged hadrons that we see?

![Jet Composition Vs. Pt](../notebooks/files/composition_combo_pt_pfpaper_final_v2.png)

<details>
<summary>Show answer...</summary>
A majority of the constituents in a jet come from pions. Pions come in neutral ($\pi^{0}$) and charged ($\pi^{\pm}$) varieties. Naively you would expect the composition to be two thirds charged hadrons and one third neutral hadrons. However, we know that $\pi^{0}$ decays to two photons, which leads to a large photon fraction.
</details>
