"""
Tango is where operation controls happen, defined here, you will find
methods ready to initialise the scrap engine, save the data in our trusty
databases and then invoke the evalator on the saved data 
"""

def saver(url=None):
	"""Officer in charge of defensive operations, commands the scrap functions
	to go and get data, in other words you could say he is in charge of reconnaisance
	:parameters: specific url to scrap from, the urls only defer in date
	:returns: boolean value or flags an error if it runs into one"""
	pass


def saver_worker(diction):
	"""saver subcommandant incharge of data verification and the actual work of saving.
	makes sure we do not have redundant info being added  to our databases"""
	# counries have unique names 
	# leagues may ahve similar names but not in the same country
	# teams may have similar names but not in the same league(i hope)
	pass

def evaluator():
	"""evaluates and decides what teams gets flagged in which classification is it placed"""
	pass
	