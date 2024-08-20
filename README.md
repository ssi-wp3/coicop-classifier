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
{
    # Which receipt items to classify
    "coicop_classification_request": ["123abc", "456def"],
    # The identified items on the receipt (products and price)
    "receipt": {
        "store": "Jumbo",
        "date": "2024-05-01",
        "items": [
            {   
                "id": "123abc",
                "description": "JUMBO LUSDRAAGTAS",
                "quantity": 1,
                "unit_price": 0.75,
                "total_price": 0.75
            },
            {
                "id": "456def",
                "description": "MINI RB ROZIJNENBOL",
                "quantity": 1,
                "unit_price": 1.79,
                "total_price": 1.79
            },
        ]
        # The total price for all items on the receipt
        "total": 2.54,
        # The currency
        "currency": "EUR",
        # An optional language hint
        "language_hint": "nl",
        # Possibly some metadata
        "metadata": null
    }
}
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

