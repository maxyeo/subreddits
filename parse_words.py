import time, sys
from abc import ABCMeta, abstractmethod
import json
import mistune
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from cs475_types import ClassificationLabel, FeatureVector, Instance

class Descriptions:
    def __init__(self):
        self.instances = []
        self.corpus = []
        self.subreddits = []
        self.descriptions = []
        self.start_time = time.clock()
        self.end_time = time.clock()
        self.cachedStopWords = stopwords.words("english")

    def load_instances(self):
        filename = "output/word_frequencies.txt"
        with open(filename) as reader:
            for line in reader:
                split_line = line.split(" ")
                label = ClassificationLabel(split_line[0])
                split_line.pop(0)
                fv = FeatureVector()
                for word in split_line:
                    if word != "\n":
                        num = word.split(":")
                        fv.add(int(num[0]),int(num[1]))
                instance = Instance(fv, label)
                self.instances.append(instance)
        return self.instances

    def create_instances(self):
        counter = 0.0
        length = len(self.descriptions)
        filename = "output/word_frequencies.txt"
        fo = open(filename, "wb")
        for d in self.descriptions:
            stripped = self.clean_text(d['description'])
            label = ClassificationLabel(int(counter))
            fv = FeatureVector()
            for word in stripped:
                feature = self.corpus.index(word)
                fv.add(feature, int(fv.get(feature) + 1))
            instance = Instance(fv, label)
            self.instances.append(instance)
            line = str(label) + " "
            for f in fv.get_keys():
                line += str(f) + ":" + str(fv.get(f)) + " "
            fo.write(line.encode('utf8') + "\n")
            counter += 1
            self.update_progress(float(counter/length))
        fo.close()

    def load_corpus_from_file(self):
        filename = "output/corpus.txt"
        # filename = "data/problem.txt"
        file_length = self.file_len(filename)
        with open(filename) as reader:
            for line in reader:
                word = line.replace("\n", "")
                self.corpus.append(unicode(word, "utf-8"))

    def corpus_to_file(self):
        counter = 0.0
        filename = "output/corpus.txt"
        length = len(self.descriptions)
        self.start_time = time.clock()
        for d in self.descriptions:
            stripped = self.clean_text(d['description'])
            for word in stripped:
                if word not in self.corpus:
                    self.corpus.append(word)
            counter += 1
            self.update_progress(float(counter/length))
        self.corpus.sort()
        fo = open(filename, "wb")
        for word in self.corpus:
            fo.write(word.encode('utf8') + "\n")
        fo.close()

    def load_descriptions_from_file(self, filename="output/descriptions.txt"):
        # filename = "data/descriptions_small.txt"
        file_length = self.file_len(filename)
        with open(filename) as reader:
            for line in reader:
                dic = json.loads(line)
                self.descriptions.append(dic)

    def load_unstopped_descriptions(self):
        self.load_descriptions_from_file("output/unstopped_descriptions.txt")
        return self.descriptions

    def unstop_descriptions(self):
        self.start_time = time.clock()
        counter = 0.0
        self.load_descriptions_from_file()
        filenameOut = "output/unstopped_descriptions.txt"
        file_length = len(self.descriptions)
        fo = open(filenameOut, "wb")
        for d in self.descriptions:
            abb_dic = {}
            abb_dic['display_name'] = d['display_name']
            abb_dic['unstopped_description'] = ' '.join([word for word in self.clean_text(d['description']) if word not in (self.cachedStopWords)])
            fo.write(json.dumps(abb_dic) + "\n")
            counter += 1
            self.update_progress(float(counter/file_length))
        fo.close()

    # only subreddits from reddituserpostingbehavior makr the file
    # only subreddits with descriptions make the file
    def descriptions_to_file(self):
        self.start_time = time.clock()
        counter = 0.0
        filename = "data/subreddits.txt"
        filenameOut = "output/descriptions.txt"
        file_length = self.file_len(filename)
        print "reading subreddits descriptions from " + filename
        fo = open(filenameOut, "wb")
        with open(filename) as reader:
            for line in reader:
                dic = json.loads(line)
                abb_dic = {}
                if dic['display_name'] in self.subreddits:
                    if dic['description']:
                        abb_dic['display_name'] = dic['display_name']
                        abb_dic['description'] = dic['description']
                        fo.write(json.dumps(abb_dic) + "\n")
                counter += 1
                self.update_progress(float(counter/file_length))
        fo.close()

    def load_subreddits_from_file(self):
        filename = "output/display_names.txt"
        file_length = self.file_len(filename)
        with open(filename) as reader:
            for line in reader:
                if len(line.strip()) == 0:
                    continue
                if "\n" in line:
                    line = line.replace("\n", "")
                self.subreddits.append(line)
        return self.subreddits

    def subreddits_to_file(self):
        self.start_time = time.clock()
        counter = 0.0
        filename = "data/data.txt"
        filenameOut = "output/display_names.txt"
        file_length = self.file_len(filename)
        print "reading subreddits from " + filename
        with open(filename) as reader:
            for line in reader:
                if len(line.strip()) == 0:
                    continue
                split_line = line.split(",")
                split_line.pop(0)
                for subreddit in split_line:
                    # sometimes there is an extraneous "\n"
                    if "\n" in subreddit:
                        subreddit = subreddit.replace("\n", "")
                    if subreddit not in self.subreddits:
                        self.subreddits.append(subreddit)
                counter += 1
                self.update_progress(float(counter/file_length))
        self.subreddits.sort()
        fo = open(filenameOut, "wb")
        for subreddit in self.subreddits:
            fo.write(subreddit + "\n")
        fo.close()

    # converts raw reddit description markdown into html, then into plaintext
    # then striped extra characters
    # if this funciton is editted, corpus should be recreated
    def clean_text(self, t):
        html = mistune.markdown(t)  # convert markdown to html
        html = html.replace("\n", " ") # replace \n characters with spaces
        cleantext = BeautifulSoup(html, 'html.parser').text # conert html to plaintext
        split_line = cleantext.split(" ")
        # print split_line
        stripped = [word.strip(",.!?;:()[]{}-+>~^\|$&\"'/=`*#") for word in split_line] # strip unwanted characters like punctuation
        stripped = [word.lower() for word in stripped]
        stripped = filter(None, stripped) # remove empty words
        return stripped

    # update_progress() : Displays or updates a console progress bar
    ## Accepts a float between 0 and 1. Any int will be converted to a float.
    ## A value under 0 represents a 'halt'.
    ## A value at 1 or bigger represents 100%
    # http://stackoverflow.com/questions/3160699/python-progress-bar
    def update_progress(self, progress):
        barLength = 10 # Modify this to change the length of the progress bar
        status = ""
        self.end_time = time.clock()
        time_elapsed = str(self.end_time - self.start_time) + "ms "
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
            status = "error: progress var must be float\r\n"
        if progress < 0:
            progress = 0
            status = "Halt...\r\n"
        if progress >= 1:
            progress = 1
            status = "Done...\r\n"
        block = int(round(barLength*progress))
        # text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
        text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, time_elapsed + status)
        sys.stdout.write(text)
        sys.stdout.flush()

    def file_len(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1


