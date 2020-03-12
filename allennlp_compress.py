from gpt2 import Gpt2Predictor
import re
from arithenco import arithencoder as ae 
import arithmeticcoding
import string      # definitions of ascii printable chars
from collections import defaultdict     # fast counting
# TODO
# Compute exact compression rate in the current scheme
# Compute the rate of the calgary corpus

d = defaultdict(int)    # define dictionary for counting frequencies
encoder = ae()
enc = arithmeticcoding.ArithmeticEncoder()

SMALL_MODEL = 'gpt2'
MEDIUM_MODEL = 'https://storage.googleapis.com/allennlp/models/gpt2-345M-dump'

#inp = input("Enter a sentence: ")
f = open("newton_large.txt", "r")
text = f.read()
#text = " how you fix it, including those of us in the news media who are trying to sort through the facts and fictions as best we can."
inp_list = re.findall(r"[\w']+|[.,!?; ]", text)

for ch in text:       # loop over each character 
    if ch in string.printable:     # is the character in the ascii/printable set?
        d[ch] += 1    #   if so, add 1 to that characters frequency counter

static_freq = []
list_dict = []

for key in d:
	static_freq.append(d[key])
	list_dict.append(key)

static_freq_arithenco = arithmeticcoding.SimpleFrequencyTable(static_freq)

gpt2_small = Gpt2Predictor(SMALL_MODEL)
#gpt2_small = Gpt2Predictor(MEDIUM_MODEL)
prev = "Newton's work "
next = ''

j = 0
not_found = ''
num_not_found = 0
#gpt2_medium = Gpt2Predictor(MEDIUM_MODEL) #This does not seem to work
print('Total number of words', len(inp_list))

while j<len(inp_list)-3:
	if(j%100 == 0):
		print("current index:", j, "total indices:", len(inp_list))
	k = 40 #Relation between k and compression ratio. Since increasing k increases the number of words found but also increases individual compression length opf arithmetic coder. 
	flag = 0
	inp = {
	'previous':prev,
	'next':next,
	'topk':k+1
	}

	output_small = gpt2_small.predict_json(inp)
	#output_medium_eg = gpt2_medium.predict_json(inp_eg)
	#print('previous:',prev)
	#print('next:',next)
	
	#print(inp_list[j])
	#print(inp_list[j]+inp_list[j+1])
	#print(output_small['words'])
	#for i in range(len(output_small['words'])):
	#	print(output_small['words'][i],':',output_small['probabilities'][i])

	if inp_list[j] in output_small['words']: #What else other than words can we use?
		index = output_small['words'].index(inp_list[j])# search for inp_list[0], if not found, then go for inp_list[1].
		keyword = inp_list[j]
		j = j + 1
	elif inp_list[j]+inp_list[j+1] in output_small['words']:	
		index = output_small['words'].index(inp_list[j]+inp_list[j+1])# search for inp_list[0], if not found, then go for inp_list[1].
		keyword = inp_list[j]+inp_list[j+1]
		j = j + 2
	else:
		#print("Not found: XOXO", inp_list[j], "or", inp_list[j+1])
		#print(output_small['words'])
		index = k+1
		keyword = inp_list[j] + inp_list[j+1]
		flag = 1
		num_not_found = num_not_found + 1
		not_found = not_found + keyword + ':'
		j = j + 2
	#print(index)
	if flag == 0:
		freqs = arithmeticcoding.SimpleFrequencyTable(output_small['probabilities'])
		enc.write(freqs, index)
		#compressed_current = encoder.compress_words(keyword, output_small['words'], output_small['probabilities'], k)
		#compressed.extend(compressed_current)
	elif flag == 1:
		for ch in keyword:
			if ch in list_dict:
				index = list_dict.index(ch)
				enc.write(static_freq_arithenco, index)	
		#print("Implement basic arithmetic coding using static frequencies")

	prev = prev + next
	next = keyword

compressed = enc.finish()
print(compressed)
print(len(compressed))
print('Number of times not found: ',num_not_found)
print('Words not found: ',not_found)
print('Total number of words', len(inp_list))
#for i in range(len(output_medium_eg['words'])):
#	print(output_medium_eg['words'][i],':',output_medium_eg['probabilities'][i])