import time, sys
from fuzzywuzzy import fuzz, process
from heapq import heappush, heappop

class Levenshtein:
	def __init__(self, instances):
		self.instances = instances
		self.descriptions = []
		for i in instances:
			self.descriptions.append(i["unstopped_description"])
		self.start_time = time.clock()
		self.end_time = time.clock()

	def train(self):
		counter = 0
		file_length = len(self.instances)
		for subreddit in self.instances:
			maxScores = []
			for subredditB in self.instances:
				if subreddit["display_name"] != subredditB["display_name"]:
					score = fuzz.partial_ratio(subreddit["unstopped_description"], subredditB["unstopped_description"])
					heappush(maxScores, (score, subredditB))
					counter += 1
					self.end_time = time.clock()
					time_elapsed = str(self.end_time - self.start_time) + "ms "
					print str(counter) + " / " + str(file_length) + " : " + time_elapsed + " " + str(score) + " " + subredditB["display_name"]
					# self.update_progress(float(counter/file_length))
			print heappop(maxScores)

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
		text = "\rPercent: [{0}] {1:.2f}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, time_elapsed + status)
		sys.stdout.write(text)
		sys.stdout.flush()
