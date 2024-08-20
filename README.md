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

## Before the installation

The `predict_coicop.py` script has been tested with Python 3.11.
Before using the script install its dependencies with:

```cli
pip install -r requirements.txt
```

This command should be executed from the root directory of this project where
the `requirements.txt` file is located.

## Training a model

If you want to train/fine-tune your own models use the `train_embedding.py` script. This script can
fine-tune an existing HuggingFace sentence-transformer with custom provided data. The data should
be put in the `input_data` folder with a format as described [here](./input_data/README.md). By default,
the `train_embedding.py` script downloads and fine-tunes a LaBSE models. Other pre-trained models can be
found [here](https://huggingface.co/sentence-transformers). It is sufficient to pass a model path to the
`-m` parameter to choose a different model, for instance `sentence-transformers/all-MiniLM-L6-v2` can
be used to download the `all-MiniLM-L6-v2` model and fine-tune it using a custom dataset.

The `train_embedding.py` script has the following parameters:

| Short Command | Long Command            | Description                                                                                     | Default                                                      |
|---------------|-------------------------|-------------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| `-i`          | `--input-filename`      | Path to the input file                                                                          | `$data_directory/input_data/ssi_hf_labse_unique_values.parquet` |
| `-o`          | `--output-directory`    | Path to the output directory                                                                    | `$data_directory/models`    |
| `-m`          | `--model-name`          | Huggingface sentence transformers model name                                                    | `"sentence-transformers/LaBSE"`                               |
| `-s`          | `--sample-size`         | Number of samples to use from the total dataset. These samples are split over train, validation and test datasets. | `None` (means all)                                                      |
| `-e`          | `--epochs`              | Number of epochs                                                                                | `3`                                                    |
| `-b`          | `--batch-size`          | Batch size                                                                                      | `32`                                                        |
| `-ic`         | `--input-column`        | Name of the input column                                                                        | `"receipt_text"`                                             |
| `-lc`         | `--label-column`        | Name of the label column                                                                        | `"coicop_number"`                                            |
| `-ef`         | `--evaluation-function` | Evaluation function                                                                             | `"f1"`                                                       |
| `-es`         | `--evaluation-strategy` | Evaluation strategy                                                                             | `"epoch"`                                                    |
| `-u`          | `--keep-unknown`        | Flag to keep unknown values, i.e. receipt texts with COICOP label 999999                                                                     | `False` (flag not set)                                       |

Note that if `$data_directory` is not set, the current directory (`.`) will be used. Note that a GPU is advised to train these models.

## Usage

The `predict_coicop.py` script can be used as follows:

```cli
python predict_coicop.py --pp models/huggingface/<model dir> -pt hugging_face -i example_receipts/jumbo_receipt1.json -o /path/to/output/folder/jumbo_receipt1_classified.json -c coicop_mapping/coicop_1999_mapping.csv
```

This command classifies all the receipt texts in `example_receipts/jumbo_receipt1.json`
and writes them to the `/path/to/output/folder/jumbo_receipt1_classified.json` file.
It furthermore uses the `coicop_mapping/coicop_1999_mapping.csv` file as a lookup table
to find descriptions for the COICOP labels found.

The `predict_coicop.py` script has the following parameters:

| Short Command | Long Command                   | Description                                      |
|---------------|--------------------------------|--------------------------------------------------|
| `-pp`         | `--pipeline-path`              | Path to pipeline                                 |
| `-pt`         | `--pipeline-type`              | Type of pipeline to use for prediction, either "hugging_face" or " sklearn", (default: "hugging_face")          |
| `-i`          | `--input-data`                 | Path to the input json file                      |
| `-o`          | `--output-data`                | Path to the output json file                     |
| `-c`          | `--coicop-code-list`           | Path to the COICOP code list/ mapping                     |
| `-d`          | `--delimiter`                  | Delimiter for the COICOP code list (default ";" )              |
| `-cc`         | `--coicop-column`              | Column name for the COICOP code in the COICOP mapping file (default: "coicop_number")                |
| `-cn`         | `--coicop-description-column`  | Column name for the COICOP name in the COICOP mapping file (default: "coicop_name" )                  |
| `-p`          | `--params`                     | Path to the params json file (optional)          |

This command should be executed from the root directory of this project where
the `predict_coicop.py` file is located.

## Input file structure

The input file structure looks as follows:

```json
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

## Output file structure

The output file contains all information from the input file and adds the classification.
This looks as follows:

```json
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
    },
    "coicop_classification_result": {
        "result": [
            {
                "id": "123abc",
                "coicop_codes": [
                    {
                        "code": "011140",
                        "description": " Overige bakkerijproducten ",
                        "confidence": 0.1767372339963913
                    },
                    {
                        "code": "011940",
                        "description": " Kant-en-klaarmaaltijden ",
                        "confidence": 0.11907301098108292
                    },
                    {
                        "code": "011830",
                        "description": " Chocolade ",
                        "confidence": 0.07663311064243317
                    },
                ...
            },
            {
            "id": "456def",
            "coicop_codes": [
                {
                    "code": "011130",
                    "description": " Brood ",
                    "confidence": 0.6990135312080383
                },
                {
                    "code": "011140",
                    "description": " Overige bakkerijproducten ",
                    "confidence": 0.23259545862674713
                },
                {
                    "code": "011830",
                    "description": " Chocolade ",
                    "confidence": 0.009536930359899998
                },
                ...
            }
        ]
    }
}
```

As can be seen in the `coicop_classification_result` part of the above JSON message, for each receipt text `id`, an array `coicop_codes`
is returned with the classifier confidence per COICOP code. For each COICOP code, also a description is given back. For instance, COICOP
011130 corresponds to "Bread" and COICOP 011830 corresponds to chocolate.

For a complete example see [classified_jumbo_receipt1.json](./example_receipts/classified_jumbo_receipt1.json)
