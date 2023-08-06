# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2017 Luzzi Valerio
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
#
# Name:        mail.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     12/03/2013
# -------------------------------------------------------------------------------
import smtplib
from smtplib import SMTP_SSL as SMTP
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from .strings import *
from .crypto import decrypt
#-------------------------------------------------------------------------------
#   mailto
#-------------------------------------------------------------------------------
def system_mail(dest,Body="",Subject=None):

    if isstring(dest):
        receivers = dest.split(",")
    if not Subject:
        Subject = Body[:16]+"[...]"

    server   = "smtps.aruba.it"
    password = decrypt('NDkgaS9KpQZJ4AHCDByp/+fArwb5IBwqNgqb/lnu9ntz/V/z02mEHs2VDtzS+6DN')
    username = decrypt('odsUxLPy/GYixv4DXiTvddQ2RCij5olwpiMMUgL+uaGPmNHeCQ6tQ99MCGUuFPkR')
    port     = 465

    msg = MIMEMultipart()
    msg['From'] = username
    msg['To']   = ",".join(receivers)
    msg['Subject'] = Subject
    msg.attach(MIMEText(Body))

    try:
        #mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer = SMTP(server,port)
        mailServer.login(username, password)
        mailServer.sendmail(username, receivers, msg.as_string())
        mailServer.close()
    except smtplib.SMTPException,ex:
        print ex
#-------------------------------------------------------------------------------
#   main
#-------------------------------------------------------------------------------
def main():
    system_mail("valerio.luzzi@gecosistema.it","This is a test smtplib message.")


if __name__ == '__main__':
    main()