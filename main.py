from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, DateTimeField, SelectField
from wtforms.fields.html5 import URLField, TimeField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    location = URLField(label='Location URL', validators=[URL()])

    open_time = TimeField(label="Open time: ",  format='%H:%M', validators=[DataRequired()])
    closing_time = TimeField(label="Closing time: ",  format='%H:%M', validators=[DataRequired()])

    coffee = SelectField(label="Coffee rating: ", choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"])
    wifi = SelectField(label="Wifi rating: ", choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"])
    power = SelectField(label="Power outlet rating: ", choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"])
    submit = SubmitField(label='Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_entry = []
        for item in form:
            new_entry.append(item.data)
        new_entry = new_entry[:7]

        with open('cafe-data.csv', "a", newline='', encoding='utf-8') as csv_file:
            csv_data = csv.writer(csv_file, delimiter=',')
            csv_data.writerow(new_entry)

        return redirect("/cafes")
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)