# Introduction

This repository contains software and data for "DeepCausalPV: A Transformer-based Causal Inference Framework for Enhancing Pharmacovigilance".
The paper describes an innovative causal inference model – DeepCausalPV, by integrating the A Lite Bidirectional Encoder Representations from Transformers (ALBERT)
 and Judea Pearl’s Do-calculus to establish potential causality in pharmacovigilance. Do-calculus mechanism has been enrolled in this software.

This software builds on
1. ALBERT: [github.com/google-research/albert](https://github.com/google-research/albert);
2. And Judea Pearl’s Do-calculus. 


# Requirements and setup

1. You'll need to download a pre-trained ALBERT model (following the above github link). We use `Base`.
2. Install Tensorflow 1.15

# Data

The FAERS case reports curated in the PharmaPendium database (https://www.pharmapendium.com/login/email) were used in this study.
1. We used the search query "Effects: [Acute liver fibrosis and cirrhosis, OR Acute liver failure and associated disorders, OR Cholestasis and jaundice]
 AND Drugs by AND-groups: [Analgesics (Any Role)]" to extract Analgesics-induced acute liver failure dataset.
For convience, you can get the dataset from https://drive.google.com/file/d/1VGGs7uxC4UiOIWFZ2LQ6N2cLweMxOSqi/view?usp=sharing
2. We employed the search query "Drugs: [Tramadol Hydrochloride] 
AND Drugs Reported Role: [Drug's Reported Role: Primary Suspect Drug OR Secondary Suspect Drug]"
 and obtained FAERS case reports for Tramadol-related mortalities.
For convience, you can get the dataset from https://drive.google.com/file/d/1VIg5vpQhk2FbAwDBwTzyJ18LyxGZ6VII/view?usp=sharing

# Reproducing the Analgesics-induced acute liver failure experiments

The default settings for the code match the settings used in the software.

1. You'll run from `src` code as 
`./Analgesics-induced_acute_liver_failure/data_processing.sh`
Before doing this, you'll need to put the datset.csv file to `dat/Analgesics-induced_acute_liver_failure/dataset/` directory.
2. Then you'll run `./Analgesics-induced_acute_liver_failure/run_ALBERT.sh`
Before doing this, you'll need to change `ALBERT_BASE_DIR=../ALBERT/model` to `ALBERT_BASE_DIR=[PATH to ALBERT MODEL]`
3. Finally, you'll run `./Analgesics-induced_acute_liver_failure/run_casual_inference.sh`, and you can find the causal results csv files in the `dat/Analgesics-induced_acute_liver_failure\causal_result`


# Reproducing the Tramadol-related_mortalities experiment

1. You'll run from `src` code as 
`./Tramadol-related mortalities/data_processing.sh`
Before doing this, you'll need to put the datset.csv file to `dat/Tramadol-related mortalities/dataset/` directory.
2. Then you'll run `./Tramadol-related mortalities/run_ALBERT.sh`
Before doing this, you'll need to change `ALBERT_BASE_DIR=../ALBERT/model` to `ALBERT_BASE_DIR=[PATH to ALBERT MODEL]`
3. Finally, you'll run `./Tramadol-related mortalities/run_casual_inference.sh`, and you can find the causal results csv files in the `dat/Tramadol-related mortalities\causal_result`

# Other FAERS dataset
Instructions for running other experiments are essentially the same as for Analgesics-induced acute liver failure



