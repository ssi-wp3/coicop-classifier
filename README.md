# Coicop Classifier

This repository contains scripts to classify products on receipt in JSON format into the their corresponding
COICOP label. The main entry point for this classification pipeline is the `predict_coicop.py` script.
To work the scripts needs a COICOP classifier model that can either be a trained `scikit-learn` or
a trained `hugging-face` NLP model. Both models should be able to process raw text and return a COICOP label
identifier. The models should be placed in the `models` directory. There are separate directories for
scikit learn models and HuggingFace models, `models/sklearn` and `models/huggingface` respectively.
Note that it is expected that both type of models return string labels for the COICOP classification.

The script can also take a CSV file that maps the corresponding COICOP labels into a human readable text.
An example file is available in the `coicop_mapping` directory. If such file is available `predict_coicop.py`
script also returns human readable descriptions as part of the predictions. Example receipts in JSON format 
are also available in the `example_receipts` directory.

## Usage

The `predict_coicop.py` script can be used as follows:

```cli

```

## Input file structure

The input file structure looks as follows:

```json

```

## Output file structure

The output file contains all information from the input file and adds the classification.
This looks as follows:

```json

```

