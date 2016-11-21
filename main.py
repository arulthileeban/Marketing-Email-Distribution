import smtplib,sys,time,sqlite3
from email.MIMEText import MIMEText
class SMTP(object):
    def SMTPconnect(self):
        print "SMTP Connect Test"
        self.server=raw_input("Enter SMTP server: ")#'smtp.gmail.com'
        self.port=input("Enter SMTP port: ")#Usually 25 or 465
        try:
            self.mailServer = smtplib.SMTP(self.server,self.port)
        except IOError, e:
            print 'Error: %s' %(e)
            time.sleep(5)
            sys.exit(1)
        self.mailServer.starttls()
        self.username=raw_input("Enter Username: ")
        self.password=raw_input("Enter Password: ")
        try:
            self.mailServer.login(self.username,self.password)
        except BaseException, e:
            print 'Error: %s' % (e)
            time.sleep(3)
            sys.exit(1)

    def buildemail(self):
        print "Marketing Email Distribution "
        self.conn=sqlite3.connect('info.db')
        self.details=self.conn.execute('select * from info')
        self.From = raw_input("From: ")
        self.Subject = raw_input("Subject: ")
        self.Message = raw_input("Message: ")
        i = 0
        for row in self.details:
            self.To=row[1]
            mimemsg = MIMEText("Dear "+row[0]+",\n"+self.Message)
            mimemsg['From']=self.From
            mimemsg['To']=row[1]
            mimemsg['Subject']=self.Subject
            self.mailServer.sendmail(self.From, self.To, mimemsg.as_string())
            i+=1
            print "Sent %d message to %s" %(i,self.To)
            time.sleep(7)
        self.conn.close()

    def builddata(self):
        print('Data Entry')
        ch=raw_input("Do you want to add records to the database(y/n)")
        if ch=='n':
            return
        else:
            n=input("Number of records to be inserted:")
            self.conn=sqlite3.connect('info.db')
            for i in xrange(n):
                name=raw_input('Enter Name: ')
                email=raw_input('Enter Email ID: ')
                self.conn.execute('INSERT INTO `info`(`Name`,`Email`) VALUES (?,?)',(name,email))
                self.conn.commit()
            self.conn.close()

if __name__ == '__main__':
    s = SMTP()
    s.builddata()
    s.SMTPconnect()
    s.buildemail()