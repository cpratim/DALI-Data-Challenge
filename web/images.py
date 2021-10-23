import json
import requests

with open('../data/DALI_Data.json', 'r') as f:
	d = json.load(f)

	for n, p in enumerate(d):
		req = requests.get(p['picture'])
		with open(f'static/images/image{n}.png', 'wb') as f:
			f.write(req.content)
