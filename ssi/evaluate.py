from typing import List
from sklearn.metrics import confusion_matrix
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_confusion_matrix(y_true: np.array, y_pred: np.array, output_path: str, labels: List[str] = None):
    # Plot and save confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    if labels:
        cm = pd.DataFrame(cm, index=labels, columns=labels)

    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt='d')
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.savefig(os.path.join(output_path, 'confusion_matrix.png'))
