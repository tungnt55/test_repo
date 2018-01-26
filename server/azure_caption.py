# my keys, expired soon
# 57fb1c5fd7d94a02b66c388f00c955ac
# 9d0c6497f2c0484bb3e508c68aa452da

####################################

########### Python 2.7 #############
import httplib, urllib, base64, json
import time
import sys

def get_azure_caption(file_name,input_caption):
	###############################################
	#### Update or verify the following values. ###
	###############################################

	# Replace the subscription_key string value with your valid subscription key.
	subscription_key = '57fb1c5fd7d94a02b66c388f00c955ac'

	# Replace or verify the region.
	#
	# You must use the same region in your REST API call as you used to obtain your subscription keys.
	# For example, if you obtained your subscription keys from the westus region, replace 
	# "westcentralus" in the URI below with "westus".
	#
	# NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
	# a free trial subscription key, you should not need to change this region.
	uri_base = 'westcentralus.api.cognitive.microsoft.com'

	headers = {
	    # Request headers.
	    'Content-Type': 'application/octet-stream',
	    'Ocp-Apim-Subscription-Key': subscription_key,
	}

	params = urllib.urlencode({
	    # Request parameters. All of them are optional.
	    'visualFeatures': 'Categories,Description,Color',
	    'language': 'en',
	})

	# The URL of a JPEG image to analyze.
	#body = "{'url':'https://upload.wikimedia.org/wikipedia/commons/1/12/Broadway_and_Times_Square_by_night.jpg'}"
	start_time = time.clock()
	try:
		# Execute the REST API call and get the response.
		conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
		f = open(file_name,'rb')
		conn.request("POST", "/vision/v1.0/analyze?%s" % params, f.read(), headers)
		response = conn.getresponse()
		data = response.read()

		# 'data' contains the JSON data. The following formats the JSON data for display.
		parsed = json.loads(data)
		#print (json.dumps(parsed, sort_keys=True, indent=2))
		#print(parsed["description"]["captions"][0]["text"])
		conn.close()
		input_caption[parsed["description"]["captions"][0]["text"]] = 0
		#print input_caption	
		return parsed["description"]["captions"][0]["text"]

	except Exception as e:
		print('Error:')
		print(e)
		return None
	#end_time = time.clock()
	#print("total run time: "+str(end_time-start_time))
	####################################

def main(args):
	###############################################
	#### Update or verify the following values. ###
	###############################################

	# Replace the subscription_key string value with your valid subscription key.
	subscription_key = '57fb1c5fd7d94a02b66c388f00c955ac'

	# Replace or verify the region.
	#
	# You must use the same region in your REST API call as you used to obtain your subscription keys.
	# For example, if you obtained your subscription keys from the westus region, replace 
	# "westcentralus" in the URI below with "westus".
	#
	# NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
	# a free trial subscription key, you should not need to change this region.
	uri_base = 'westcentralus.api.cognitive.microsoft.com'

	headers = {
	    # Request headers.
	    'Content-Type': 'application/octet-stream',
	    'Ocp-Apim-Subscription-Key': subscription_key,
	}

	params = urllib.urlencode({
	    # Request parameters. All of them are optional.
	    'visualFeatures': 'Categories,Description,Color',
	    'language': 'en',
	})

	# The URL of a JPEG image to analyze.
	#body = "{'url':'https://upload.wikimedia.org/wikipedia/commons/1/12/Broadway_and_Times_Square_by_night.jpg'}"
	start_time = time.clock()
	try:
		# Execute the REST API call and get the response.
		conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
		f = open(args[1],'rb')
		conn.request("POST", "/vision/v1.0/analyze?%s" % params, f.read(), headers)
		response = conn.getresponse()
		data = response.read()

		# 'data' contains the JSON data. The following formats the JSON data for display.
		parsed = json.loads(data)
		print ("Response:")
		#print (json.dumps(parsed, sort_keys=True, indent=2))
		print(parsed["description"]["captions"][0]["text"])
		conn.close()

	except Exception as e:
		print('Error:')
		print(e)
	end_time = time.clock()
	print("total run time: "+str(end_time-start_time))
	####################################

if __name__ == "__main__":
	main(sys.argv)
