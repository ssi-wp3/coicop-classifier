# Input Data

Please put your input data here. The input data should be an Apache Parquet file with at
least two columns containing the receipt text and the coicop label. If you want to use
the `train_embedding.py` script without passing additional arguments for the column names:

- the receipt text column should be named `receipt_text`
- the label column should be named `coicop_number`
