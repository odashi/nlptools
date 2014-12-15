# -*- coding: utf-8 -*-
#
# Backpropagation algorithm for 3-layer perceptron.
# Usage:
#   reg = FeedForwardNN(num_feature, num_answer, num_hidden, training_factor)
#   for feature_list, answer_list in training_data:
#     reg.train(feature_list, answer_list)
#   for feature_list in test_data:
#     y_list = reg.predict(feature_list)
# 

import math
import random

class FeedForwardNN3:

 	def __init__(self, num_input, num_output, num_hidden, eta):
		self.__ni = num_input
		self.__no = num_output
		self.__nh = num_hidden
		self.__eta = eta
		self.__whi = [[random.uniform(-1.0, 1.0) for i in range(self.__ni)] for h in range(self.__nh)]
		self.__woh = [[random.uniform(-1.0, 1.0) for h in range(self.__nh)] for o in range(self.__no)]
		self.__wh0 = [random.uniform(-1.0, 1.0) for h in range(self.__nh)]
		self.__wo0 = [random.uniform(-1.0, 1.0) for o in range(self.__no)]
		# temporary
		self.__vh = [0 for h in range(self.__nh)]
		self.__vo = [0 for o in range(self.__no)]
		self.__eh = [0 for h in range(self.__nh)]
	
	@staticmethod
	def __sigmoid(x):
		if x > 0.0:
			return 1.0 / (1.0 + math.exp(-x))
		else:
			ex = math.exp(x)
			return ex / (ex + 1.0)

	@staticmethod
	def __forward(vx, vy, w, w0, nx, ny):
		for y in range(ny):
			tmp = w0[y]
			for x in range(nx):
				tmp += w[y][x] * vx[x]
			vy[y] = Perceptron3.__sigmoid(tmp)
	
	def train(self, feature, answer):
		Perceptron3.__forward(feature, self.__vh, self.__whi, self.__wh0, self.__ni, self.__nh)
		Perceptron3.__forward(self.__vh, self.__vo, self.__woh, self.__wo0, self.__nh, self.__no)

		for h in range(self.__nh):
			self.__eh[h] = 0

		for o in range(self.__no):
			tmp = (self.__vo[o] - answer[o]) * self.__vo[o] * (1 - self.__vo[o])
			for h in range(self.__nh):
				self.__eh[h] += tmp * self.__woh[o][h]

			self.__wo0[o] -= self.__eta * tmp
			for h in range(self.__nh):
				self.__woh[o][h] -= self.__eta * tmp * self.__vh[h]

		for h in range(self.__nh):
			tmp = self.__eh[h] * self.__vh[h] * (1 - self.__vh[h])

			self.__wh0[h] -= self.__eta * tmp
			for i in range(self.__ni):
				self.__whi[h][i] -= self.__eta * tmp * feature[i]

	def predict(self, feature):
		Perceptron3.__forward(feature, self.__vh, self.__whi, self.__wh0, self.__ni, self.__nh)
		Perceptron3.__forward(self.__vh, self.__vo, self.__woh, self.__wo0, self.__nh, self.__no)
		return self.__vo.copy()

	def printStatus(self):
		print('3-layer perceptron:')
		print('  %d inputs, %d outputs, %d hiddens' %
				(self.__ni, self.__no, self.__nh))
		print('  Learning factor: %.4f' % self.__eta)
		
		print('  Input-hidden weights:')
		print('    bias:', end='')
		for h in range(self.__nh):
			print(' %+.3f' % self.__wh0[h], end='')
		print()
		for i in range(self.__ni):
			print('    %4d:' % (i+1), end='')
			for h in range(self.__nh):
				print(' %+.3f' % self.__whi[h][i], end='')
			print()

		print('  Hidden-output weights:')
		print('    bias:', end='')
		for o in range(self.__no):
			print(' %+.3f' % self.__wo0[o], end='')
		print()
		for h in range(self.__nh):
			print('    %4d:' % (h+1), end='')
			for o in range(self.__no):
				print(' %+.3f' % self.__woh[o][h], end='')
			print()
