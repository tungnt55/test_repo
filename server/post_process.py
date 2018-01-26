from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
#from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import sys
import random

LANGUAGE = "english"
SENTENCES_COUNT = 7

class Box:
	x = 0.0
	y = 0.0
	width = 0.0
	height = 0.0
	position = ""

	def __init__(self):
		return

	def __init__(self, new_x, new_y, new_width, new_height):
		self.init(new_x, new_y, new_width, new_height)
		return

	def init(self, new_x, new_y, new_width, new_height):
		self.x = new_x
		self.y = new_y
		self.width = new_width
		self.height = new_height
		center = self.x + new_width/2
		if center < 240.0:
			self.position = "left"
		elif center < 480.0:
			self.position = "front"
		else:
			self.position = "right" 
		return
	
	def tostring(self):
		return str(self.x)+" "+str(self.y)+" "+str(self.width)+" "+str(self.height)

def summarize_file(file_name):
	#url = "http://www.zsstritezuct.estranky.cz/clanky/predmety/cteni/jak-naucit-dite-spravne-cist.html"
	#parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
	# or for plain text files
	parser = PlaintextParser.from_file(file_name, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)

	summarizer = Summarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)
	
	sentences = summarizer(parser.document, SENTENCES_COUNT)
	list_sentences = []
	for sentence in sentences:
		list_sentences.append(str(sentence))
	return list_sentences

def paraphrase(captions_boxes_map):
	for sentence in captions_boxes_map.keys():
		tmp_sentence = sentence
		sentence_spl = sentence.split(" ")
		corresponding_box = captions_boxes_map[sentence]
		if sentence_spl[0] == "the":
			tmp_sentence.replace("the","there is a",1)
		if sentence_spl[0] == "a":
			tmp_sentence = "there is "+tmp_sentence
		if sentence_spl[0] in ["people","two"]:
			tmp_sentence = "there are "+tmp_sentence
		if sentence_spl[0] == "man":
			tmp_sentence = "there is a "+tmp_sentence
		random_value = random.random()
		if corresponding_box.position == "left":
			if random_value < 0.25:
				tmp_sentence = tmp_sentence+" to the left"
			elif random_value < 0.5:
				tmp_sentence = tmp_sentence+" to your left"
			elif random_value < 0.75:
				tmp_sentence = "to the left, "+tmp_sentence
			else:
				tmp_sentence = "to your left, "+tmp_sentence
		if corresponding_box.position == "front":
			if random_value < 0.25:
				tmp_sentence = tmp_sentence+" in front of you"
			elif random_value < 0.5:
				tmp_sentence = tmp_sentence+" to the front"
			elif random_value < 0.75:
				tmp_sentence = "to the front, "+tmp_sentence
			else:
				tmp_sentence = "in front of you, "+tmp_sentence
		if corresponding_box.position == "right":
			if random_value < 0.25:
				tmp_sentence = tmp_sentence+" to the right"
			elif random_value < 0.5:
				tmp_sentence = tmp_sentence+" to your right"
			elif random_value < 0.75:
				tmp_sentence = "to the right, "+tmp_sentence
			else:
				tmp_sentence = "to your right, "+tmp_sentence
		captions_boxes_map[tmp_sentence] = captions_boxes_map.pop(sentence)
	return
   
def post_process_captions():	 
	captions = []
	boxes = []
	captions_boxes_map = {}

	captions_file = open("captions.txt","r")
	refs = captions_file.read().rstrip().splitlines()
	while "" in refs:
		refs.remove("")
	#print(refs)
	captions = refs
	captions_file.close()
	
	boxes_file = open("boxes.txt","r")
	refs = boxes_file.read().rstrip().splitlines()
	while "" in refs:
		refs.remove("")
	while "[torch.CudaTensor of size 4]" in refs:
		refs.remove("[torch.CudaTensor of size 4]")
	#print(refs)
	for i in xrange(0,len(refs)-1,4):
		tmp_box = Box(float(refs[i]),float(refs[i+1]),float(refs[i+2]),float(refs[i+3]))
		boxes.append(tmp_box)
		
	for i in xrange(len(captions)):
		captions_boxes_map[captions[i][:-1]] = boxes[i]
	
	#for key, value in captions_boxes_map.iteritems():
	#	print(key, value.tostring())
	paraphrase(captions_boxes_map)
	#for key, value in captions_boxes_map.iteritems():
	#	print(key)
	
	caption_file = open("new_captions.txt","w")
	for key in captions_boxes_map.keys():
		caption_file.write(key+".\n")
	caption_file.close()
	#for sentence in summarize_file("new_captions.txt"):
	#	print(sentence)
	return summarize_file("new_captions.txt")

def main(args):
	#print (summarize_file("captions.txt"))
	captions = []
	boxes = []
	captions_boxes_map = {}

	captions_file = open("captions.txt","r")
	refs = captions_file.read().rstrip().splitlines()
	while "" in refs:
		refs.remove("")
	#print(refs)
	captions = refs
	captions_file.close()
	
	boxes_file = open("boxes.txt","r")
	refs = boxes_file.read().rstrip().splitlines()
	while "" in refs:
		refs.remove("")
	while "[torch.CudaTensor of size 4]" in refs:
		refs.remove("[torch.CudaTensor of size 4]")
	#print(refs)
	for i in xrange(0,len(refs)-1,4):
		tmp_box = Box(float(refs[i]),float(refs[i+1]),float(refs[i+2]),float(refs[i+3]))
		boxes.append(tmp_box)
		
	for i in xrange(len(captions)):
		captions_boxes_map[captions[i][:-1]] = boxes[i]
	
	#for key, value in captions_boxes_map.iteritems():
	#	print(key, value.tostring())
	paraphrase(captions_boxes_map)
	#for key, value in captions_boxes_map.iteritems():
	#	print(key)
	
	caption_file = open("new_captions.txt","w")
	for key in captions_boxes_map.keys():
		caption_file.write(key+".\n")
	caption_file.close()
	for sentence in summarize_file("new_captions.txt"):
		print(sentence)
	
	return		
	
if __name__ == "__main__":
	main(sys.argv)
