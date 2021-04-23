from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from create_reaction_dict import html_table

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def home():
    return render_template('home.html', table=html_table)

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    print(processed_text)

if __name__ == '__main__':
    app.run()