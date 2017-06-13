import urlparse

def parseFormData(rawData):
	data = {}
	formData = urlparse.parse_qsl(rawData)

	for dataset in formData:
		data[dataset[0]] = dataset[1].decode('utf-8')

	return data
