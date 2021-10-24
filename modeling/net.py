import os

import torch
from torch import nn
from torch import optim
import torch.nn.functional as F
from tqdm import tqdm

import numpy as np
from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler,
)
from sklearn.pipeline import Pipeline
from gplearn.genetic import SymbolicTransformer
import pickle

sk_pipeline = Pipeline(
    [
        ('scaler', StandardScaler()),
        #('transformer', SymbolicTransformer(n_jobs=-1))
    ]
)

def correlation(x, y):
    return np.corrcoef(x, y)[0, 1]

class LinearNet(nn.Module):

    def __init__(self, n_feat, n_out= 1):

        super().__init__()

        self.conv1 = nn.Conv1d(n_feat, 15, 1)
        self.pool1 = nn.MaxPool1d(1)
        self.flatten = nn.Flatten()
        self.relu1 = nn.ReLU()
        self.linear1 = nn.Linear(15, 5)
        self.out = nn.Linear(5, n_out)

    def forward(self, x):
        x = self.conv1(x)
        x = self.pool1(x)
        x = self.flatten(x)
        x = self.relu1(x)
        x = self.linear1(x)
        x = self.out(x)
        return x


def train(
    model,
    X, y,
    epochs=50000,
    batch_size=None,
    learning_rate=1e-5,
    score_func=correlation,
    optimizer=optim.Adam,
    loss_func=nn.MSELoss(),
):
        
    y_comp = y.detach().cpu().numpy().reshape(-1,)
    optimizer = optimizer(model.parameters(), lr=learning_rate)
    splits = floor(len(X) / batch_size) if batch_size != None else 1

    X_batches = torch.tensor_split(X, splits)
    y_batches = torch.tensor_split(y, splits)
    bar = tqdm(range(epochs))
    for epoch in bar:
        for x, y in zip(X_batches, y_batches):
            y_pred = model(x)
            loss = loss_func(y_pred, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        y_pred_comp = model(X).detach().cpu().numpy().reshape(-1,)
        score = score_func(y_pred_comp, y_comp)
        bar.set_description(f"Score: {round(score, 5)}")
    
    return model


class ModelWrapper(object):

    def __init__(self, model = LinearNet, train_func = train, feature_pipeline = sk_pipeline, **kwargs):

        self.model = model(**kwargs)
        self.train_func = train_func
        self.feature_pipeline = feature_pipeline
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    def fit(self, X, y, **kwargs):
        
        X = self.feature_pipeline.fit_transform(X, y)
        y = y.reshape(-1, 1)
        X = X.reshape(-1, X.shape[1], 1)
        X = torch.Tensor(X)
        y = torch.Tensor(y)
        X = X.to(self.device)
        y = y.to(self.device)
        self.model = self.model.to(self.device)
        self.model = self.train_func(self.model, X, y, **kwargs)

    def detach(self, y):
        return y.detach().cpu().numpy().reshape(-1,)

    def predict(self, X):
        
        X = self.feature_pipeline.transform(X)
        X = X.reshape(-1, X.shape[1], 1)
        X = torch.Tensor(X)
        X = X.to(self.device)
        y = self.model(X)
        return self.detach(y)  

    def save(self, dir):
        with open(dir, 'wb') as f:
            pickle.dump(self, f)
