import sys
import glob
from BeautifulSoup import *
import json
import sqlite3

num_args = len(sys.argv)
if num_args == 1:
    output = sys.argv
if num_args > 2:
    print "Pass either no parameters to see summary or \'json\' or \'sql\' as \
a single parameter to output these formats"


def get_files(target_dir, file_spec = '*'):
    td = target_dir
    fs = file_spec
    try:
        files = glob.glob(td + '*' + fs + '*')
    except glob_error as e:
        return None
    return files

def create_insert(table,fields,data):
    ''' This is completely insecure and needs to be replaced with proper
        format strings to pass the strings through the review of the connector
    '''
    field_count = len(fields)
    if field_count <> len(data):
        return None
    ctr = 0
    sql = 'INSERT into ' + table + '('
    for field in fields:
        if ctr <> field_count - 1:
            sql += field + ','
        else:
            sql += field + ') values('
        ctr += 1
    ctr = 0
    for d in data:
        if ctr <> field_count - 1:
            sql += "'" + d + "',"
        else: 
            sql += "'" + d + "')"
        ctr += 1
            
    
    return sql

class  HtmPage(object):
    ''' A page is a single raw collection of html
    ''' 
    def __init__(self,file_name):
        ''' Initiates a page object with the contents of a file
        '''
        try:
            fname = open(file_name, 'r')
        except IOError:
            print ('cannot open file:' + file_name)
            self.contents = None
            self.name = "I/O Error inititializing HtmPage object"
           
            return None
        else:
            self.contents = fname.read().strip(' \t\n\r')
            dot_slash = './'
            self.name = file_name.replace(dot_slash,"")
            self.size=len(self.contents)
            self.htm_tags = []
            self.values = {}

    def getName(self):
        return self.name
    
    def getLength(self):
        if self.contents is None:
            return None
        else:
            return len(self.contents)

    def getTags(self,tag):
        ''' provides page object with set of beautiful soap
            tag objects and stores
            them as a list in instance.htm_tags
        '''
        
        if self.contents is None:
            return None
        else:
            bsObj = BeautifulSoup(self.contents)
            self.htm_tags = bsObj.findAll(tag)
        
    def getValues(self,tag):
        ''' returns key, val tuple from tag by parsing on the first ":" char
        '''
        if self.contents is None:
            return None
        else:
            tag_text = tag.text
            pos = tag_text.find(":")
            #split on first ":", clean leading and trailing whitespace
            k = tag_text[0:pos].strip(' \t\n\r')
            v = tag_text[pos+1:].strip(' \t\n\r')
            return (k,v)
    
    def getWarc(self):
        return None
        
    def __str__(self):
        return self.name        



#look in the current directory for files
fspec = 'meta'
path = './' 
files = get_files(path,fspec)
#dict of HtmPage objects
mypages = {}

#fill the mypages dict with page instances
ctr = 0
for f in files:
    mypages[ctr] = HtmPage(f)
    ctr += 1
#print 'We have ', str(ctr), ' instances in mypages{}'

#dump the pages to a json struct
''' This is done before populating the tag objects onto the HtmPage
    objects as they complicate the scruture and will not dump to json without
    further work.'''
jstruct = ''
for page in mypages:
    jstruct += json.dumps(mypages[page].__dict__)

#print jstruct


# fill the for page instances htm_tags list:
tag_type = 'li'
for p in mypages:
    mypages[p].getTags(tag_type)



sql = ''
for p in mypages:
    ''' loop through the pages and 
        construct the value lists for SQL insert
    '''

    table = 'Pages'
    field_count = 0
    
    #first field in list is not in k,v pairs, it is the key identifying the page
    pageID = mypages[p].name
    field_list = ["PageID"]
    data_list = []
    #Each value statment starts with the foreign key of pageID
    data_list.append(pageID)
    for t in mypages[p].htm_tags:

        ''' loop through the tags and 
            construct the field list and value lists for SQL insert
        '''
        #table = 'Tags'
        k,v = mypages[p].getValues(t)
        field_list.append(k.replace(" ","_"))
        data_list.append(v)
        field_count += 1
        
        
    
    sql += create_insert('Tags',field_list,data_list) + ";\n"

if num_args == 1:
    report = 'We found ' + str(len(files)) + ' ' + fspec + ' files in ' + path + ' and ' + str(len(mypages))
    report +=  ' page instances'
    num_tags = 0
    for p in mypages:
        num_tags += len(mypages[p].htm_tags)
    report += ' containing a total of ' + str(num_tags) + ' tags of type ' + tag_type
    print report

elif sys.argv[1] == 'json':
        print jstruct
elif sys.argv[1] == 'sql':
        print sql
else:
    print "Unknown format " + sys.argv[1]
