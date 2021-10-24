from modeling.load import load_numerical
import numpy as np
from scipy.stats import mode
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from modeling.net import ModelWrapper
import json
from pprint import pprint
import pickle

def correlation(x, y):
	return np.corrcoef(x, y)[0, 1]

test_size = .2
X, features = load_numerical()

datasets = {}

p = X.T
for n, f in enumerate(features):
	y = p[n]
	p = np.delete(p, n, axis=0)
	
	datasets[f] = {
		'X': p.T, 'y': y,
	}
	p = X.T

binary = ['gender', 'affiliated', 'phoneType']

models = {}
for fn in features:
	with open(f'modeling/models/{fn}.model', 'rb') as f:
		models[fn] = pickle.load(f)

def load_features():
	return features

def load_feature_ranges():
	ranges = {}
	for x, f in zip(X.T, features):
		if f=='heightInches':
			ranges[f] = list(range(50, max(x)+1))
		else:
			ranges[f] = list(range(min(x), max(x)+1))
	return ranges

def train_models():
	model_stats = {}
	n_fits = 10
	for f in datasets:
		print(f'TRAINING: [{f}]')
		best_corr = 0
		best_acc = 0
		best_model = None
		for i in range(n_fits):
			m = datasets[f]
			model = ModelWrapper(n_feat = 13)
			X_train, X_test, y_train, y_test = train_test_split(m['X'], m['y'], test_size=test_size)
			model.fit(X_train, y_train, epochs=10000, learning_rate=1e-5)

			pred = model.predict(X_test)
			corr = correlation(pred, y_test)
			acc = len([0 for y1, y2 in zip(pred, y_test) if round(y1) == round(y2)])/len(y_test)
			if f in binary:
				if acc > best_acc:
					best_acc = acc
					best_model = model
					best_corr = corr
			else:
				if corr > best_corr:
					best_acc = acc
					best_corr = corr
					best_model = best_model
			if best_model == None:
				best_model = model
				best_corr = corr
				best_acc = acc
		
		best_model.save(f'modeling/models/{f}.model')
		model_stats[f] = {'correlation': best_corr, 'accuracy': best_acc}
		print(f'BEST ACC: {round(best_acc, 3)} | BEST CORR: {round(best_corr, 3)}')


	with open('modeling/model_stats.json', 'w') as f:
		json.dump(model_stats, f)

def predict(feat, X):
	x = []
	for f, v in X.items():
		if f != feat:
			x.append(v)
	x = np.array([x,])
	return models[feat].predict(x)