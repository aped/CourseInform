#!/usr/bin/env python
""" 
CourseInform, a scaled back and less ambitious version of CourseGrab. 
by Andrew Pedelty
"""

import getpass
import mechanize
import cookielib
import time
import sys
import smtplib
from email.mime.text import MIMEText


# Generic globals, because lazy
WAIT_TIMER = 45      # Time between queries in seconds. Don't be rude, keep it 30+s
ROOTURL = "pisa.ucsc.edu/class_search"
# Hardcoded because kludge; there's a more nuanced way to do this, but for now just paste in the class URL
URL = """https://pisa.ucsc.edu/class_search/index.php?action=detail&class_data=YTozMDp7czo0OiJTVFJNIjtzOjQ6IjIxMzAiO3M6OToiQ0xBU1NfTkJSIjtzOjU6IjQyNDMxIjtzOjEzOiJDTEFTU19TRUNUSU9OIjtzOjI6IjAxIjtzOjEzOiJDTEFTU19NVEdfTkJSIjtzOjE6IjEiO3M6MTI6IlNFU1NJT05fQ09ERSI7czoxOiIxIjtzOjEwOiJDTEFTU19TVEFUIjtzOjE6IkEiO3M6NzoiU1VCSkVDVCI7czo0OiJDTVBTIjtzOjExOiJDQVRBTE9HX05CUiI7czo0OiIgMTIxIjtzOjU6IkRFU0NSIjtzOjE5OiJNb2JpbGUgQXBwbGljYXRpb25zIjtzOjEzOiJTU1JfQ09NUE9ORU5UIjtzOjM6IkxFQyI7czoxMDoiU1RBUlRfVElNRSI7czo3OiIwNDowMFBNIjtzOjg6IkVORF9USU1FIjtzOjc6IjA1OjQ1UE0iO3M6OToiRkFDX0RFU0NSIjtzOjE1OiJQb3J0ZXIgQWNhZCAxNDgiO3M6MzoiTU9OIjtzOjE6Ik4iO3M6NDoiVFVFUyI7czoxOiJZIjtzOjM6IldFRCI7czoxOiJOIjtzOjU6IlRIVVJTIjtzOjE6IlkiO3M6MzoiRlJJIjtzOjE6Ik4iO3M6MzoiU0FUIjtzOjE6Ik4iO3M6MzoiU1VOIjtzOjE6Ik4iO3M6OToiRU5STF9TVEFUIjtzOjE6IkMiO3M6ODoiV0FJVF9UT1QiO3M6MToiMCI7czo4OiJFTlJMX0NBUCI7czoyOiI2MCI7czo4OiJFTlJMX1RPVCI7czoyOiI2MSI7czo5OiJMQVNUX05BTUUiO3M6OToiRGUgQWxmYXJvIjtzOjEwOiJGSVJTVF9OQU1FIjtzOjQ6Ikx1Y2EiO3M6MTE6Ik1JRERMRV9OQU1FIjtOO3M6MTY6IkNPTUJJTkVEX1NFQ1RJT04iO3M6MToiICI7czo1OiJUT1BJQyI7TjtzOjEyOiJESVNQTEFZX05BTUUiO3M6MTI6IkRlIEFsZmFybyxMLiI7fQ%3D%3D"""

# Email auth globals
EMAIL_UNAME = ""                # Example: "apedelty@ucsc.edu"
EMAIL_ADDRESS = ""              # <Phone number>@<email-to-sms-addr>
EMAIL_PASS = ""                 # Leave blank imo
SMTP_ADDY = "smtp.gmail.com"    # SMTP server where you'll be 
SMTP_PORT = 587

def setup_browser(debug=False):
    # Browser
    br = mechanize.Browser(factory=mechanize.RobustFactory())

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(False)           # True produces warnings, fuck it.
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Want debugging messages?
    br.set_debug_http(debug)
    br.set_debug_redirects(debug)
    br.set_debug_responses(debug)

    # User-Agent (grey hat here i comes)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    return br


def lookup_and_search(url, br): 
    resp = br.open(url)
    text = resp.readlines()
    print text[266]
    return 'open' in text[266] # MAGIC NUMBA: TODO fix this nonsense


def email_confirmation(): 
    s = smtplib.SMTP(SMTP_ADDY, SMTP_PORT)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(EMAIL_UNAME, EMAIL_PASS)
    s.sendmail(EMAIL_UNAME, EMAIL_ADDRESS, "COURSE IS AVAILABLE !!!")
    s.quit()


if __name__ == "__main__":
    counter = 1
    EMAIL_PASS = getpass.getpass("Input email password: ")
    try: 
        s = smtplib.SMTP(SMTP_ADDY, SMTP_PORT)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(EMAIL_UNAME, EMAIL_PASS)
        s.quit()
    except: 
        print "Error accessing smpt server %s." % SMTP_ADDY
        sys.exit(1)
    browser = setup_browser()
    while(lookup_and_search(URL, browser) != True):
        print "Completed attempt #%d, waiting %d seconds..." % (counter, WAIT_TIMER)
        counter += 1
        time.sleep(WAIT_TIMER)
        print "Done waiting. "
    email_confirmation()

