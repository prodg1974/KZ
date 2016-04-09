import glob
from BeautifulSoup import *
import json
import sqlite3

def get_files(target_dir, file_spec = '*'):
    td = target_dir
    fs = file_spec
    try:
        files = glob.glob(td + '*' + fs + '*')
    except glob_error as e:
        return None
    return files

class  HtmPage(object):
    '''
    A page is a single raw collection of html
    ''' 
    def __init__(self,file_name):
        '''Initiates a page object with the contents of a file
        '''
        try:
            fname = open(file_name, 'r')
        except IOError:
            print ('cannot open file:' + file_name)
            self.contents = None
            self.name = "I/O Error inititializing HtmPage object"
           
            return None
        else:
            self.contents = fname.read().replace('\n', '')
            self.name = file_name
            self.size=len(self.contents)
            self.htm_tags = []
    def __str__(self):
        return self.name
    def getName(self):
        return self.name
    
    def getLength(self):
        if self.contents is None:
            return None
        else:
            return len(self.contents)

    def getTags(self,tag):
        '''provides page object with set of beautiful soap
        tag objects and stores
        them as a list in instance.tags'''
        
        if self.contents is None:
            return None
        else:
            bsObj = BeautifulSoup(self.contents)
            self.htm_tags = bsObj.findAll(tag)
        
    def getWarcHash(self):
        return None
    
    def getWarc(self):
        return None
        
        



#look in the current directory for files
files = get_files('./', 'meta')
#dict of HtmPage objects
mypages = {}

#fill the dict
ctr = 0
for f in files:
    mypages[ctr] = HtmPage(f)
    ctr += 1
print 'We have ', str(ctr), ' page objects in mypages{}'

#dump the pages to a json struct
''' This is done before populating the tag objects onto the HtmPage
    objects as they complicate the scruture and will not dump to json without
    further work.'''
jstruct = ''
for page in mypages:
    jstruct += json.dumps(mypages[page].__dict__)

print jstruct
