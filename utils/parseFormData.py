def parseFormData(rawData):
	formData = rawData.split('&')
	data = {}
	
	for i in formData:
		param = i.split('=')
		data[param[0]] = param[1]

	return data


def parseFormData1(rawData):
	formData = rawData.split('&')
	data = {}
	
	for i in formData:
		param = i.split('=')
		data[param[0]] = param[1]

	return data
