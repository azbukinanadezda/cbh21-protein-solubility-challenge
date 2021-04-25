"""
The entry point for your prediction algorithm.
"""

#from __future__ import annotations
import argparse
import csv
import itertools
from pathlib import Path
import pprint
from typing import Any
import zipfile

import temppathlib



import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
import lightgbm as lgbm
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
import pathlib
import json 

from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr
from sklearn.feature_selection import RFECV



def predict(pdb_file):
    """
    The function that puts it all together: parsing the PDB file, generating
    features from it and performing inference with the ML model.
    """

    
    # featurize + perform inference
    features = featurize(pdb_file)
    predicted_solubility = ml_inference(features)

    return predicted_solubility

def read_model(filename):
  with open(filename, 'rb') as file:
    clf = pickle.load(file)
  return(clf)
  
def prediction(clf, x_test):
  y_pred = clf.predict(x_test)
  return(y_pred)
  

def featurize(pdb_file):
    """
    Calculates 3D ML features from the `structure`.
    """
    df = pd.read_csv('features_model.csv', index_col = [0]) 
    # read feature file (we generated it in advance for all available pdbs in this task)
    # description of features is available in README.md
    df['protein'] = df.index
    features = df[df['protein'] == pdb_file.stem]
    # choose query pdb
    features = features.drop(columns=['protein'])
    
    return features


def ml_inference(features):
    """
    This would be a function where you normalize/standardize your features and
    then feed them to your trained ML model (which you would load from a file).
    """
    # read model
    clf = read_model('model.pkl')
    y_pred = prediction(clf, features)
    return y_pred[0]


if __name__ == "__main__":

    # set up argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", type=str, default="data/test.zip")
    args = parser.parse_args()

    predictions = []
    # use a temporary directory so we don't pollute our repo
    with temppathlib.TemporaryDirectory() as tmpdir:
        # unzip the file with all the test PDBs
        with zipfile.ZipFile(args.infile, "r") as zip_:
            zip_.extractall(tmpdir.path)

        # iterate over all test PDBs and generate predictions
        for test_pdb in tmpdir.path.glob("*.pdb"):
            predictions.append({"protein": test_pdb.stem, "solubility": predict(test_pdb)})

    # save to csv file, this will be used for benchmarking
    outpath = "predictions.csv"
    with open(outpath, "w") as fh:
        writer = csv.DictWriter(fh, fieldnames=["protein", "solubility"])
        writer.writeheader()
        writer.writerows(predictions)

    # print predictions to screen
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(predictions)
