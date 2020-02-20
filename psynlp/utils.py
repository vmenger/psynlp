import pkg_resources
import os
import psydata

def get_local_resource(resource_path):
    return pkg_resources.resource_filename('psynlp', os.path.join('resources', resource_path))

def get_global_resource(resource_path):

	### TODO: refer this path to a folder where you store: 
	# * A spacy model in the /spacy directory (different models can be specified when using the package)
	# * A gensim model in the /gensim directory called word2vec.model
	# * A token_frequencies.csv file that is ;-separated and contains a "token" and "frequency" column
	
	GLOBAL_RESOURCE_PATH = "C:/Documents" # change this line

    return os.path.join(GLOBAL_RESOURCE_PATH, resource_path) # don't change this line

class SentenceStream(object):    
    def __init__(self, filenames, maxrows=None):
        self.filenames = filenames # List, not a string
        self.maxrows = maxrows

    def process_lines(self, filename):
        
        # Counter so we don't stream sentences than the max
        counter = 0
        
        # Open file
        for line in open(filename, 'r'):

            # Check number of files that are read
            if counter == self.maxrows:
                break
            counter += 1
                
            # Split line
            line = line[:-1].split(" ")
                
            # Yield line
            yield line
        
    # Iterate over all filenames in the list of filenames
    def __iter__(self):
        for filename in self.filenames:
            yield from self.process_lines(filename)

