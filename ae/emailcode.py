import smtplib
from email.message import EmailMessage

def sendEmail(SEND_EMAIL_ADDR,msg_sub,msg_content):

    try:
     #with smtplib.SMTP('smtp.gmail.com',587) as smtp :
      #with smtplib.SMTP('localhost',1000) as smtp :
       #smtp.ehlo()
       #smtp.starttls()  # Encrypting the connection
       #smtp.ehlo()

       #using SSL From begining 

      with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp :
       EMAIL_ADDR='alientronicsindia@gmail.com'
       PASS='ckbwphjnduwkoayr'
       TO_EMAIL=SEND_EMAIL_ADDR
       smtp.login(EMAIL_ADDR,PASS)

       msg=EmailMessage()
       #msg['Subject'] = 'Welcome to Alientronics'
       msg['Subject']= msg_sub
       msg['From']=EMAIL_ADDR
       msg['To']= TO_EMAIL
       #msg.set_content('Dear User, \n Welcome to Alientronics India.\n We are glad to have you on board. \n\n\n\n Best Regards, \n Alientronics Team')
       msg.set_content(msg_content)
      

       smtp.send_message(msg)
       print('Email has been Successfully sent')
       
       smtp.quit()

       print('Connection Closed.')

    except:
        print('Exception occurred during send EMAIL')


def sendEmailNew(To_ADDR):
      EMAIL_ADDR='alientronicsindia@gmail.com'
      PASS='rtuqxasriplexvws'

      # building the message body
      # using new email Message Body

      msg=EmailMessage()
      msg['Subject'] = 'Welcome to Alientronics'
      msg['From']=EMAIL_ADDR
      msg['To']= To_ADDR
      msg.set_content('Dear User, \n Welcome to Alientronics India.\n We are glad to have you on board.\n sent from new message \n \n\n\n\n Best Regards, \n Alientronics Team')
      print('Sending Message ....')

      try :
      # SENDING TO LOCAL SERVER
       with smtplib.SMTP('localhost', 1000) as smtp:

         smtp.send_message(msg)
         print('Email has been Successfully sent')
       
         smtp.quit()

         print('Connection Closed.')
      except:
        print('!! Exceptions occurred !!')

def sendEmailDebug(TO_EMAIL):

    try:
       with smtplib.SMTP('localhost',1000) as smtp : 
        EMAIL_ADDR='alientronicsindia@gmail.com'
        TO_EMAIL=TO_EMAIL
        subject ='Welcome To Alientronics'
        body= 'Dear User, \n Welcome to Alientronics India.\n We are glad to have you on board. \n sent from new message \n \n\n\n\n Best Regards, \n Alientronics Team'
        msg=f'Subject: {subject} \n\n{body}'

        smtp.sendmail(EMAIL_ADDR,TO_EMAIL,msg)
        print('Email has been Successfully sent')
       
        smtp.quit()

        print('Connection Closed.')
        # debug server sudo python3 -m smtpd -c DebuggingServer -n localhost:1000

    except:
       print('Exceptions happened during send Email')

# For testing 
#msg_content='This is a dynamic message'
#sub='Complaint Raised Successfully'
#sendEmail('parikshit_majumder@outlook.com',sub,msg_content)   
#sendEmailDebug('parikshit_majumder@outlook.com')   
# 
#sendEmailNew('parikshit_majumder@outlook.com') 