from abc import ABCMeta, abstractmethod
import json
import markdown
from bs4 import BeautifulSoup

class Descriptions:
    def __init__(self):
        self.instances = []
        self.dictionary = []
        self.file_length = 0

    def load(self, filename):
        self.file_length = self.file_len(filename)
        counter = 0
        with open(filename) as reader:
            for line in reader:
                dic = json.loads(line)
                if dic['description']:
                    print dic['display_name']
                    html = markdown.markdown(dic['description'])  # convert markdown to html
                    html = html.replace("\n", " ") # replace \n characters with spaces
                    cleantext = BeautifulSoup(html, 'html.parser').text # conert html to plaintext
                    split_line = cleantext.split(" ")
                    # print split_line
                    stripped = [word.strip(",.!?;:()[]{}->~^\|$&\"*#") for word in split_line] # strip unwanted characters like punctuation
                    stripped = filter(None, stripped) # remove empty words
                    for word in stripped:
                        if word not in self.dictionary:
                            self.dictionary.append(word)
                counter += 1
                print str(counter) + "/" + str(self.file_length)
            # print self.dictionary
            print len(self.dictionary)

    def file_len(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1


