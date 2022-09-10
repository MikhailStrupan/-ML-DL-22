import re
import os
import random
import pickle
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='N-gramm text generation')
    parser.add_argument('--input_dir', default='', help='The path to the directory where the document collection'
                                                        ' is located.If this argument is not given,'
                                                        ' get from input (default: )')
    parser.add_argument('--model', help='The path to the file in which the model is saved.If empty, '
                                        'the file to save will be created (default: )')

    return parser.parse_args()


class TextGenerator:

    def __init__(self, file_path='', dict_path=''):
        self.file_path = file_path
        self.dict_path = dict_path

    def list_from_file(self, file):
        file_path = f"{self.file_path}/{file}"
        with open(file_path, 'r') as f:
            return re.sub(r'[^A-Za-z]', " ", f.read()).lower().split()

    def all_texts_together(self):
        if self.file_path == '':
            return input().split()

        os.chdir(self.file_path)
        all_texts = []
        for file in os.listdir():
            if file.endswith(".txt"):
                all_texts.append(self.list_from_file(file))

        return all_texts

    def monograms(self):
        dict_of_monograms = {}
        all_texts = self.all_texts_together()
        for text in all_texts:
            for ind in range(len(text) - 1):
                if text[ind] not in dict_of_monograms:
                    dict_of_monograms[text[ind]] = []
                dict_of_monograms[text[ind]].append(text[ind + 1])

        dict_of_monograms_prob = {}
        for key in dict_of_monograms:
            last = {}
            for word in dict_of_monograms[key]:
                if word not in last:
                    last[word] = 0
                last[word] += 1
            for ind in last:
                last[ind] = last[ind] / len(last)
            last_1 = sorted(last.items(), key=lambda x: -x[1])
            dict_of_monograms_prob[key] = last_1

        return dict_of_monograms_prob

    def bigrams(self):
        dict_of_bigrams = {}
        all_texts = self.all_texts_together()
        for text in all_texts:
            for ind in range(len(text) - 2):
                if (text[ind], text[ind + 1]) not in dict_of_bigrams:
                    dict_of_bigrams[(text[ind], text[ind + 1])] = []
                dict_of_bigrams[(text[ind],
                                 text[ind + 1])].append(text[ind + 2])

        dict_of_bigrams_prob = {}
        for key in dict_of_bigrams:
            last = {}
            for word in dict_of_bigrams[key]:
                if word not in last:
                    last[word] = 0
                last[word] += 1
            for ind in last:
                last[ind] = last[ind] / len(last)
            last_1 = sorted(last.items(), key=lambda x: -x[1])
            dict_of_bigrams_prob[key] = last_1

        return dict_of_bigrams_prob

    def fit(self):
        dict_of_monograms_prob = self.monograms()
        dict_of_bigrams_prob = self.bigrams()
        with open(self.dict_path, 'wb') as f:
            pickle.dump(dict_of_monograms_prob, f)
            pickle.dump(dict_of_bigrams_prob, f)

    @staticmethod
    def choose_from_monogram(dict_of_monograms, message):
        key = message[-1]
        if key in dict_of_monograms and len(dict_of_monograms[key]) >= 10:
            choosen_results = dict_of_monograms[key][0:10]
            choosen_index = random.randint(0, len(choosen_results) - 1)
            choosen_word = choosen_results[choosen_index][0]
            message.append(choosen_word)
        elif key in dict_of_monograms:
            message.append(dict_of_monograms[key][0][0])
        else:
            choosen_results = random.choice(list(dict_of_monograms.values()))
            choosen_index = random.randint(0, len(choosen_results) - 1)
            choosen_word = choosen_results[choosen_index][0]
            message.append(choosen_word)
        return message

    @staticmethod
    def choose_from_bigrams(dict_of_bigrams, dict_of_monograms, message):
        key = (message[-2], message[-1])
        if key in dict_of_bigrams and len(dict_of_bigrams[key]) >= 10:
            choosen_results = dict_of_bigrams[key][0:10]
            choosen_index = random.randint(0, len(choosen_results) - 1)
            choosen_word = choosen_results[choosen_index][0]
            message.append(choosen_word)
        elif key in dict_of_bigrams:
            message.append(dict_of_bigrams[key][0][0])
        else:
            TextGenerator.choose_from_monogram(dict_of_monograms, message)
        return message

    @staticmethod
    def generate(message, length, dict_path):
        with open(dict_path, 'rb') as f:
            dict_of_monograms = pickle.load(f)
            dict_of_bigrams = pickle.load(f)

        for i in range(length - len(message)):
            if len(message) > 1:
                TextGenerator.choose_from_bigrams(dict_of_bigrams,
                                                  dict_of_monograms, message)
            if len(message) == 1:
                TextGenerator.choose_from_monogram(dict_of_monograms, message)
            if len(message) == 0:
                choosen_results = random.choice(
                    list(dict_of_monograms.values()))
                choosen_index = random.randint(0, len(choosen_results) - 1)
                choosen_word = choosen_results[choosen_index][0]
                message.append(choosen_word)

        return ' '.join(message)


if __name__ == '__main__':
    args = parse_args()
    generator = TextGenerator(args.input_dir, args.model)
    generator.fit()
