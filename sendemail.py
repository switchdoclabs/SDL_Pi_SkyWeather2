import traceback


def sendEmail(source, message, subject, toaddress, fromaddress, filename):


	# Check for user imports
        import config
        import pclogging

	# Import smtplib for the actual sending function
        import smtplib

        # Here are the email package modules we'll need
        from email.mime.image import MIMEImage
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        COMMASPACE = ', '

	# Create the container (outer) email message.
        msg = MIMEMultipart()
        msg['Subject'] = subject 
	# me == the sender's email address
	# family = the list of all recipients' email addresses
        msg['From'] = fromaddress
        msg['To'] =  toaddress
	#msg.attach(message) 

        mainbody = MIMEText(message, 'plain')
        msg.attach(mainbody)

	# Assume we know that the image files are all in PNG format
    	# Open the files in binary mode.  Let the MIMEImage class automatically
       	# guess the specific image type.
        if (filename != ""):
                fp = open(filename, 'rb')
                img = MIMEImage(fp.read())
                fp.close()
                msg.attach(img)

	# Send the email via our own SMTP server.

        try:
            if (config.SWDEBUG):
                pclogging.systemlog(config.INFO, "--->sending mail<---")    
            # open up a line with the server
            s = smtplib.SMTP(config.mailServer, 587)
            s.ehlo()
            s.starttls()
            s.ehlo()

            # login, send email, logout
            s.login(config.mailUser, config.mailPassword)
            s.sendmail(config.mailUser, toaddress, msg.as_string())
            #s.close()


            s.quit()

        except:
                try:
                        pclogging.errorlog("smtp failed", traceback.format_exc()) 
                except:     
                        print(traceback.format_exc()) 
                        print ("--------------------")
                        print ("SkyCam Picture Failed")
                        print ("--------------------")
        return 0