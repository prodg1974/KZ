import smtplib
TO = 'paul_rodgers@me.com'
SUBJECT = 'Testing email from Python'

CONTENT = 'this is my message'
FROM = 'paul_rodg@yahoo.com'


mail = smtplib.SMTP('smtp.mail.yahoo.com',587)
mail.ehlo()
mail.starttls()
BODY = '\r\n'.join([
     'To: %s' % TO,
     'From: %s' % FROM,
     'Subject: %s' % SUBJECT,
     '',
     CONTENT
     ])
try:
     mail.login('paul_rodg@yahoo.com','')
     print 'logged in'
except:
     print 'login failed'
try:
     mail.sendmail(FROM, [TO], BODY)
     print 'mail sent'
except:
     print 'send failed'
mail.close

