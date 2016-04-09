import PyPDF2
mypdf = '/Users/paulr/Documents/Work/Upwork/test.pdf'
pdfFileObj = open(mypdf, 'rb')
pdfReader =  PyPDF2.PdfFileReader(pdfFileObj)
print(pdfReader.numPages)
pageObj = pdfReader.getPage(0)
myText = (pageObj.extractText())
#print myText[0:19]
i=0
for x in myText:
 i = i +1
 if x == "#":
  print("start:", str(i))
  for y in myText[i:i+15]:
    print(y, ord(y))

