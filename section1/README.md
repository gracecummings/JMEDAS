# Jet Basics

This preliminary exercise will illustrate some of the basic properties of jets in CMS. Let's start by running the histogram-making code on some $t\bar{t}$ MC. While the script is running, take a look at the script and make sure you understand what it's doing.

```
python $CMSSW_BASE/src/Analysis/JMEDAS/scripts/jmedas_make_histograms.py --files=$CMSSW_BASE/src/Analysis/JMEDAS/data/MiniAODs/RunIIFall17MiniAODv2/ttjets2023.txt --outname=$CMSSW_BASE/src/Analysis/JMEDAS/notebooks/files/ttjets.root --maxevents=2000 --maxjets=6 --maxFiles 2
```

Now let's plot the resulting histograms. Take a look at the simple plotting script below and execute it with

```
python basics.py
```
You can open the produced pdf file with evince:

```
evince plots1.pdf&
```

Your histograms from the script should look similar to the four plots shown below. What about AK8 jets? Add the corresponding histograms to the same canvases, they are already filled and available (draw option 'same', line color 'ROOT.kRed').
Open basics.py with a code editor, such as gedit, emacs, nano or vim, add the needed lines for AK8 and reproduce the plots.

![Basic jet kinematics](../files/plots1.png)