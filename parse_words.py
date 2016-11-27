import time, sys
from abc import ABCMeta, abstractmethod
import json
import markdown
from bs4 import BeautifulSoup


class Descriptions:
    def __init__(self):
        self.instances = []
        self.dictionary = []
        self.subreddits = []
        self.descriptions = []
        self.start_time = time.clock()
        self.end_time = time.clock()

    def load(self):
        counter = 0.0
        length = len(self.descriptions)
        self.start_time = time.clock()
        for d in self.descriptions:
            html = markdown.markdown(d['description'])  # convert markdown to html
            html = html.replace("\n", " ") # replace \n characters with spaces
            cleantext = BeautifulSoup(html, 'html.parser').text # conert html to plaintext
            split_line = cleantext.split(" ")
            # print split_line
            stripped = [word.strip(",.!?;:()[]{}-+>~^\|$&\"'/=`*#") for word in split_line] # strip unwanted characters like punctuation
            stripped = [word.lower() for word in stripped]
            stripped = filter(None, stripped) # remove empty words
            for word in stripped:
                if word not in self.dictionary:
                    self.dictionary.append(word)
            counter += 1
            self.update_progress(float(counter/length))
        self.dictionary.sort()
        # for word in self.dictionary:
        #     print word
        # print self.dictionary
        print len(self.dictionary)

    def load_descriptions_from_file(self):
        counter = 0.0
        filename = "output/descriptions.txt"
        file_length = self.file_len(filename)
        with open(filename) as reader:
            for line in reader:
                dic = json.loads(line)
                self.descriptions.append(dic)

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


