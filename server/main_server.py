# main server file
#!/usr/bin/env python
# Simple HTTP Server With Upload.

import os
import posixpath
import BaseHTTPServer
import urllib
import cgi
import shutil
import mimetypes
import re
import json

try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

import sys
import time
import resource
import multiprocessing
from azure_caption import get_azure_caption
from dense_caption import densecap_from_file
from post_process import post_process_captions

def perform_captioning(image_filename):
	manager = multiprocessing.Manager()
	return_dict = manager.dict()
	#azure_caps = get_azure_caption(args[1])
	#azure_process = multiprocessing.Process(target=get_azure_caption,args=(image_filename,return_dict))
	#densecap_from_file(args[1])
	densecap_process = multiprocessing.Process(target=densecap_from_file,args=(image_filename,))

	#azure_process.start()
	densecap_process.start()
	#azure_process.join()
	densecap_process.join()
	
	dense_caps = post_process_captions()
	#azure_caps = return_dict.keys()[0]
	
	#print(azure_caps)
	#for caption in dense_caps:
	#	print(caption)
	
	result_captions = ""
	#result_captions += azure_caps+" "
	for caption in dense_caps:
		result_captions += caption+" "
	return result_captions
	
class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):	
	# Simple HTTP request handler with POST commands.
	file_extension = ""
	
	def do_POST(self):
		"""Serve a POST request."""
		r, info = self.deal_post_data()
		print r, info, "by: ", self.client_address
		f = StringIO()
		
		if r:
			f.write("<strong>Success:</strong>")
		else:
			f.write("<strong>Failed:</strong>")

		length = f.tell()
		#f.seek(0)
		#data = {'sender':   'Alice','receiver': 'Bob','message':  'We did it!'}
		data = {'captions':perform_captioning("tmp.jpg")}	
		data_json = json.dumps(data)
			
		print data_json
		
		self.send_response(200)

		self.send_header("Content-type", "text/html")
		self.send_header("Content-Length", str(len(data_json)))
		self.end_headers()
		
		
		self.wfile.write(str(data_json))
		#if f:
		#	self.copyfile(f, self.wfile)
		#	f.close()
		return

	def deal_post_data(self):
		print self.headers
		boundary = self.headers.plisttext.split("=")[1]
		
		print 'Boundary %s' %boundary
		remainbytes = int(self.headers['content-length'])
		print "Remain Bytes %s" %remainbytes
		line = self.rfile.readline()
		remainbytes -= len(line)
		if not boundary in line:
			return (False, "Content NOT begin with boundary")
		line = self.rfile.readline()
		remainbytes -= len(line)
		fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line)
		if not fn:
			return (False, "Can't find out file name...")
		path = self.translate_path(self.path)
		fn = os.path.join(path, fn[0])
		print "remainbytes: ",remainbytes
		try:
			#out = open(fn, 'wb')
			out = open("tmp.jpg",'wb')
		except IOError:
			return (False, "Can't create file to write, do you have permission to write?")
		
		while line.strip():
			print "line strip true: ",line.strip(),len(line)
			line = self.rfile.readline()
			remainbytes -= len(line)
			preline = line
		else:
			print "line strip false: ",line.strip()
			preline = self.rfile.readline()		
		remainbytes -= len(preline)
		
		while remainbytes > 0:
			line = self.rfile.readline()
			remainbytes -= len(line)
			#print preline
			if boundary in line:
				preline = preline[0:-1]
				if preline.endswith('\r'):
					preline = preline[0:-1]
				out.write(preline)
				out.close()
				return (True, "File '%s' upload success!" % fn)
			else:
				out.write(preline)
				preline = line
		return (False, "Unexpect Ends of data.")

	def translate_path(self, path):
		"""Translate a /-separated PATH to the local filename syntax.

		Components that mean special things to the local file system
		(e.g. drive or directory names) are ignored.  (XXX They should
		probably be diagnosed.)

		"""
		# abandon query parameters
		path = path.split('?',1)[0]
		path = path.split('#',1)[0]
		path = posixpath.normpath(urllib.unquote(path))
		words = path.split('/')
		words = filter(None, words)
		path = os.getcwd()
		for word in words:
			drive, word = os.path.splitdrive(word)
			head, word = os.path.split(word)
			if word in (os.curdir, os.pardir): continue
			path = os.path.join(path, word)
		return path

	def copyfile(self, source, outputfile):
		"""Copy all data between two file objects.

		The SOURCE argument is a file object open for reading
		(or anything with a read() method) and the DESTINATION
		argument is a file object open for writing (or
		anything with a write() method).

		The only reason for overriding this would be to change
		the block size or perhaps to replace newlines by CRLF
		-- note however that this the default server uses this
		to copy binary data as well.

		"""
		shutil.copyfileobj(source, outputfile)



def main(HandlerClass = SimpleHTTPRequestHandler,ServerClass = BaseHTTPServer.HTTPServer):
	BaseHTTPServer.test(HandlerClass, ServerClass)

if __name__ == '__main__':
	main()
