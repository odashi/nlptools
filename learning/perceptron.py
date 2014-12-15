# -*- coding: utf-8 -*-

from collections import defaultdict


def binary_inner_product(weight_dict, feature_list):
    return sum((weight_dict[x] if x in weight_dict else 0.0) for x in feature_list)


class Perceptron:
    def __init__(self, num_classes):
        self.__num_classes = num_classes
        self.__weights = [{} for i in range(num_classes)]
    
    def predict(self, feature_list):
        best_class = -1
        best_score = -1e100
        for i in range(self.__num_classes):
            score = binary_inner_product(self.__weights[i], feature_list)
            if score > best_score:
                best_class = i
                best_score = score
        return best_class

    @staticmethod
    def load(filename):
        with open(filename) as fp:
            num_classes = int(next(fp))
            ret = Perceptron(num_classes)
            for i in range(num_classes):
                num_weights = int(next(fp))
                W = ret.__weights[i]
                for j in range(num_weights):
                    ls = next(fp).split()
                    k = ls[0]
                    v = float(ls[1])
                    W[k] = v
            return ret

    def num_classes(self):
        return self.__num_classes


class AveragedPerceptronTrainer:
    def __init__(self, num_classes):
        self.__num_classes = num_classes
        self.__weights = [defaultdict(lambda: 0.0) for i in range(num_classes)]
        self.__cumulative = [defaultdict(lambda: 0.0) for i in range(num_classes)]
        self.__num_trained = 0
        self.__learn_strength = 1.0
    
    def __update_weights(self, class_id, feature_list, delta):
        W = self.__weights[class_id]
        CW = self.__cumulative[class_id]
        n = self.__num_trained
        eta = self.__learn_strength
        for feature in feature_list:
            W[feature] += eta * delta
            CW[feature] += n * eta * delta

    def __predict(self, feature_list):
        best_class = -1
        best_score = -1e100
        for i in range(self.__num_classes):
            score = binary_inner_product(self.__weights[i], feature_list)
            if score > best_score:
                best_class = i
                best_score = score
        return best_class

    def predict(self, feature_list):
        best_class = -1
        best_score = -1e100
        for i in range(self.__num_classes):
            score \
                = binary_inner_product(self.__weights[i], feature_list) \
                - binary_inner_product(self.__cumulative[i], feature_list) / self.__num_trained
            if score > best_score:
                best_class = i
                best_score = score
        return best_class

    def train(self, answer_class, feature_list):
        self.__num_trained += 1
        best_class = self.__predict(feature_list)
        #print('n: %d, best: %d, answer: %d, features: %s' % (self.__num_trained, best_class, answer_class, ' '.join(feature_list)))
        if (best_class != answer_class):
            self.__update_weights(answer_class, feature_list, 1)
            self.__update_weights(best_class, feature_list, -1)
        return best_class

    def save(self, filename):
        EPS = 1e-10
        n = self.__num_trained
        with open(filename, 'w') as fp:
            fp.write('%d\n' % self.__num_classes)
            for i in range(self.__num_classes):
                W = self.__weights[i]
                CW = self.__cumulative[i]
                W2 = {}
                for k in W:
                    w = W[k] - CW[k] / n
                    if abs(w) > EPS:
                        W2[k] = w
                fp.write('%d\n' % len(W2))
                for k, v in W2.items():
                    fp.write('%s\t%.8e\n' % (k, v))

    def num_classes(self):
        return self.__num_classes

    def view_stats(self):
        print('num_classes    = %2d' % self.__num_classes)
        print('num_trained    = %2d' % self.__num_trained)
        print('learn_strength = %9.6f' % self.__learn_strength)
        for i in range(self.__num_classes):
            print('class %d:' % i)
            W = self.__weights[i]
            CW = self.__cumulative[i]
            for k in sorted(W):
                print('  %8s : w = %9.6f, u = %9.6f' % (k, W[k], CW[k]))


class L1RegularizedPerceptronTrainer:
    def __init__(self, num_classes, regularize_strength = 1e-3):
        self.__num_classes = num_classes
        self.__weights = [defaultdict(lambda: 0.0) for i in range(num_classes)]
        self.__last_updated = [defaultdict(lambda: 0) for i in range(num_classes)]
        self.__num_updated = [0 for i in range(num_classes)]
        self.__learn_strength = 1.0
        self.__regularize_strength = regularize_strength
    
    def __regularize(self, class_id, feature_list):
        W = self.__weights[class_id]
        U = self.__last_updated[class_id]
        n = self.__num_updated[class_id]
        penalty_unit = self.__learn_strength * self.__regularize_strength
        for feature in feature_list:
            w = W[feature]
            penalty = penalty_unit * (n - U[feature])
            if w >= 0.0:
                w = w - penalty if w > penalty else 0.0
            else:
                w = w + penalty if w < penalty else 0.0
            W[feature] = w
            U[feature] = n
    
    def __update_weights(self, class_id, feature_list, delta):
        W = self.__weights[class_id]
        U = self.__last_updated[class_id]
        n = self.__num_updated[class_id]
        eta = self.__learn_strength
        r = self.__regularize_strength
        for feature in feature_list:
            W[feature] += eta * delta
        self.__num_updated[class_id] += 1

    def predict(self, feature_list):
        best_class = -1
        best_score = -1e100
        for i in range(self.__num_classes):
            self.__regularize(i, feature_list)
            score = binary_inner_product(self.__weights[i], feature_list)
            if score > best_score:
                best_class = i
                best_score = score
        return best_class

    def train(self, answer_class, feature_list):
        best_class = self.predict(feature_list)
        #print('n: %d, best: %d, answer: %d, features: %s' % (self.__num_trained, best_class, answer_class, ' '.join(feature_list)))
        if (best_class != answer_class):
            self.__update_weights(answer_class, feature_list, 1)
            self.__update_weights(best_class, feature_list, -1)
        return best_class

    def save(self, filename):
        # regularize all features
        for i in range(self.__num_classes):
            self.__regularize(i, self.__weights[i].keys())
        EPS = 1e-10
        with open(filename, 'w') as fp:
            fp.write('%d\n' % self.__num_classes)
            for i in range(self.__num_classes):
                W = self.__weights[i]
                W2 = {}
                for k in W:
                    w = W[k]
                    if abs(w) > EPS:
                        W2[k] = w
                fp.write('%d\n' % len(W2))
                for k, v in W2.items():
                    fp.write('%s\t%.8e\n' % (k, v))

    def num_classes(self):
        return self.__num_classes

    def view_stats(self):
        print('num_classes         = %2d' % self.__num_classes)
        print('learn_strength      = %9.6f' % self.__learn_strength)
        print('regularize_strength = %9.6f' % self.__regularize_strength)
        for i in range(self.__num_classes):
            print('class %d:' % i)
            print('  num_updated = %d' % self.__num_updated[i])
            W = self.__weights[i]
            U = self.__last_updated[i]
            for k in sorted(W):
                print('  %8s : w = %9.6f, u = %2d' % (k, W[k], U[k]))

