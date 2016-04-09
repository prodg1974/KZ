import glob
def get_files(target_dir, file_spec = '*')
    td = target_dir
    fs = file_spec
    return glob.glob(td + fs )

class  HtmPage(object)
    '''
    A page is a single raw collection of html
    ''' 
    def __init__(self,file_name)
        '''Initiates a page object with the contents of a file
        '''
        fname = open(file_name, 'r')
        self.contents = ***SLURP***

    def getWarc(self)
        

    def getWarcHash(self)
        


