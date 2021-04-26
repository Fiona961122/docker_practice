"""app.py

Simple Web interface and API to spaCy entity recognition.

Usage via the API (on the local host):

$> curl http://127.0.0.1:5000/api
$> curl -H "Content-Type: text/plain" -X POST -d@input.txt http://127.0.0.1:5000/api

For the web pages point your browser at http://127.0.0.1:5000

"""


from flask import Flask, request, render_template
from flask_restful import Resource, Api
from bs4 import BeautifulSoup

import db, ner

app = Flask(__name__)
api = Api(app)


# For the website we use the regular Flask functionality and serve up HTML pages.

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('form.html', input=open('input.txt').read())
    else:
        text = request.form['text']
        markup = ner.entity_markup(text)
        soup = BeautifulSoup(markup, features='html.parser')
        entity_names = [ent.text for ent in soup.find_all('entity')]
        connection = db.DatabaseConnection('spacy.sqlite')
        connection.create_schema()
        for entity in entity_names:
            connection.add(entity)
        markup_paragraphed = ''
        for line in markup.split('\n'):
            if line.strip() == '':
                markup_paragraphed += '<p/>\n'
            else:
                markup_paragraphed += line
        return render_template('result.html', markup=markup_paragraphed)


@app.route('/entities', methods=['GET'])
def list_entity():
    connection = db.DatabaseConnection('spacy.sqlite')
    pairs = connection.get()
    table = ''
    for pair in pairs:
        table += '\t<tr>\n\t\t<td>' + pair[0] + '</td>\n\t\t<td>' + str(pair[1]) + '</td>\n\t</tr>\n'
    return render_template('entity.html', table=table)



# But for the API we use the RESTful extension and return JSON.

class EntityParserAPI(Resource):

    def get(self):
        content = "Content-Type: text/plain"
        url = 'http://127.0.0.1:5000/api'
        return \
            {"description": "Interface to the spaCy entity extractor",
             "usage": 'curl -v -H "%s" -X POST -d@input.txt %s' % (content, url)}

    def post(self):
        text = str(request.get_data(as_text=True))
        markup = ner.entity_markup(text)
        return {"input": text,
                "output": markup}, 201


api.add_resource(EntityParserAPI, "/api")


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')
