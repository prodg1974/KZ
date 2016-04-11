This code is designed to process a set of HTM files. It creates an instance of a page object for each file and parses the text of the page for a set of tags which become a property of the instance.  Values for path './', filespec '*meta*' and tag 'li' are hard coded.

Executing the script with no parameters will generate a summary report. Passing a parameter of 'json' will output the page instances in json format (but without the tags), passing a parameter of sql will ouput sql designed to insert the parsed text of the tags into a 'Tags' table.

These samples require a few modules (BeautifulSoup, json). They represent a complete environment.  After installing virtualenv, activate this environment with . ./bin/activate

I hope that I've demonstrated an understanding of coding, pytyon, and provided some insight as to my technical abilities.
