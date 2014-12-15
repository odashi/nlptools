# -*- coding: utf-8 -*-


'''
ARPA formatted language model (LM)
USAGE:
	import arpa
	ngram = 'foo bar baz'.split()
	sentence = 'this is also a sample sentence'.split()
	
	lm = arpa.LM('your_lm.arpa', default_backoff=-42, unknown_bias=-42)
	cp = lm.condprob(ngram)
	jp = lm.jointprob(sentence)
'''


from collections import defaultdict
from numbers import Real


class LM:
	'''
	ARPA formatted language model (LM)
	'''

	def __init__(self, filepath, **kwargs):
		'''
		initialize LM object.
		@param self LM object
		@param filepath (str) path of the ARPA file
		@param [kwargs]encoding (str) encoding of ARPA file (default: 'utf-8')
		@param [kwargs]default_backoff (Real) default backoff corfficient (default: -5.0)
		@param [kwargs]unknown_bias (Real) bias for log-probability of unknown word (default: 0.0)
		'''
		
		DEFAULT_ENCODING = 'utf-8'
		DEFAULT_BACKOFF = -5.0
		DEFAULT_UNK_BIAS = 0.0
		
		def getkwarg(key, type, default):
			if key in kwargs and isinstance(kwargs[key], type):
				return kwargs[key]
			else:
				return default
		
		encoding = getkwarg('encoding', str, DEFAULT_ENCODING)
		self.__backoff = float(getkwarg('default_backoff', Real, DEFAULT_BACKOFF))
		self.__unk = float(getkwarg('unknown_bias', Real, DEFAULT_UNK_BIAS))
		self.__wid = defaultdict(lambda: len(self.__wid))
		self.__maxn = 0
		
		self.__table = {}
		with open(filepath, encoding=encoding) as fp:
			for line in fp:
				ls = line.strip().split('\t')
				if not (2 <= len(ls) <= 3) or ls[0] == 'ngram':
					continue
				elif ls[1] == '<unk>':
					self.__unk += float(ls[0])
				else:
					prob = float(ls[0])
					ngram = tuple(self.__wid[x] for x in tuple(ls[1].split(' ')))
					backoff = float(ls[2]) if len(ls) == 3 else self.__backoff
					self.__table[ngram] = (prob, backoff)
					self.__maxn = max(self.__maxn, len(ngram))
		
#		print('backoff', self.__backoff)
#		print('unk', self.__unk)
#		for k,v in self.__table.items():
#			print(k,v)


	def __condprob_inner(self, ngram):
		'''
		inner calculation for LM.condprob()
		'''
		
#		print(ngram)
	
		if ngram in self.__table:
			# stored n-gram
			return self.__table[ngram][0]
		else:
			if len(ngram) == 1:
				# unknown unigram
				return self.__unk
			else:
				# backoff
				prob = self.__condprob_inner(ngram[1:len(ngram)])
				context = ngram[0:len(ngram)-1]
				if context in self.__table:
					return prob + self.__table[context][1]
				else:
					return prob + self.__backoff


	def maxn(self):
		'''
		retrieve max length of stored n-gram.
		@return (int) max length of stored n-gram.
		'''
		
		return self.__maxn


	def condprob(self, ngram):
		'''
		retrieve conditional log-probability of given n-gram:
		log(P(w[n] | w[1..n-1])).
		@param ngram tuple or list of str describing specific n-gram, or str (unigram).
		@return (float) value describing conditional log-probability of given n-gram.
		'''
		
		# check argument
		if isinstance(ngram, str):
			ngram = (ngram,)
		elif isinstance(ngram, list):
			ngram = tuple(ngram)
		elif not isinstance(ngram, tuple):
			raise TypeError('ngram must be str, tuple or list.')
		
		return self.__condprob_inner(tuple(self.__wid[x] for x in ngram))


	def jointprob(self, sentence):
		'''
		retrieve joint log-probability of given sentence:
		log(P(w[1..n])) = log(P(w[1])) + log(P(w[2] | w[1])) + ... + log(P(w[n] | w[n-k+1..n-1])),
		where k = LM.maxn().
		@param sentence tuple or list of str describing specific sentence, or str (unigram).
		@return (float) value describing joint log-probability of given sentence.
		'''
		
		# check argument
		if isinstance(sentence, str):
			sentence = (sentence,)
		elif isinstance(sentence, list):
			sentence = tuple(sentence)
		elif not isinstance(sentence, tuple):
			raise TypeError('sentence must be str, tuple or list.')
		
		# sum conditional probabilities
		k = self.__maxn
		ret = 0
		for i in range(len(sentence)):
			ngram = tuple(self.__wid[x] for x in sentence[max(i-k+1, 0):i+1])
			ret += self.__condprob_inner(ngram)
			
#			print(ngram)
		
		return ret
