

def build_heatmap(data, features):

	heatmap = {}
	for n1, f1 in enumerate(data.T):
		for n2, f2 in enumerate(data.T):
			heatmap[f'{features[n1]} x {features[n2]}'] = correlation(f1, f2)

	return heatmap

if __name__ == '__main__':

	data, features = load_numerical()
	f1, f2 = features.index('affiliated'), features.index()
	hmap = build_heatmap(data, features)
	for k, v in hmap.items():
		print(f'{k}: {v}')