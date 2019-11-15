#!/usr/bin/python3

import requests
import json
import glob, os

from flask import Flask, render_template
from werkzeug.utils import redirect
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from keypad import Keypad

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config["TEMPLATES_AUTO_RELOAD"] = True
app_capacity = 10
hourList = {}

class MyForm(FlaskForm):
    membershipNo = StringField('membershipNo', validators=[DataRequired()])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lounge/<lounge_name>', methods=('GET', 'POST'))
def submit(lounge_name=None):
    form = MyForm()
    
    for file in glob.glob("~/hackthon/lounge-bouncer-app/*.hour"):
        print("reading {}".format(file))
        hour = os.path.basename(file).replace('.hour', '')
        print("hour {}".format(hour))
        content = open(file, "r").read()
        print("content: {}".format(content))
        hourList[hour] = content

    if form.validate_on_submit():
        print('form valid')
        return redirect('/success')
    else:
        print('form not valid')
    return render_template('lounge_access.html', form=form, lounge_name=lounge_name, hourlist=hourList)


@app.route('/success', methods=('GET', 'POST'))
def success():
    return render_template('success.html')


@app.route('/guests', methods=('GET', 'POST'))
def guests():
    kp = Keypad(column_count=4)  # waiting for a keypress
    digit = None
    while digit == None:
        digit = kp.get_key()
    # Print result
    print(digit)
    guest_count = digit
    print(guest_count)
    return render_template('index.html')


@app.route('/capacity')
def capacity():
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'X-Cisco-Meraki-API-Key': '86c458f08e922045e6260cfcb06b8b76aabf2d3b',
    }

    response = requests.get('https://api.meraki.com/api/v0/devices/Q2FV-K7QZ-K7B5/camera/analytics/live',
                            headers=headers,
                            verify=False)

    response = json.dumps(json.loads(response.content)["zones"]["0"]["person"])
    print("Camera responded with body count = {}".format(response))
    app_bodycount = float(response)
    capacity_percentage = (app_bodycount / app_capacity) * 100
    print("Calculated capacity percentage: = {}".format(capacity_percentage))
    return str(capacity_percentage)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
