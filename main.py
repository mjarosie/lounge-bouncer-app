from flask import Flask, render_template
from werkzeug.utils import redirect
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config["TEMPLATES_AUTO_RELOAD"] = True

class MyForm(FlaskForm):
    membershipNo = StringField('membershipNo', validators=[DataRequired()])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lounge/<lounge_name>', methods=('GET', 'POST'))
def submit(lounge_name=None):
    form = MyForm()
    if form.validate_on_submit():
        print('form valid')
        return redirect('/success')
    else:
        print('form not valid')
    return render_template('lounge_access.html', form=form, lounge_name=lounge_name)


@app.route('/success', methods=('GET', 'POST'))
def success():
    return render_template('success.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
