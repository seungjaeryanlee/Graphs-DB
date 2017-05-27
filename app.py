from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import json
import random
from forms import FullForm, RadioField
from wtforms.validators import DataRequired

def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    return app

# Parse data.json
with open('data.json') as data_file:
    data = json.load(data_file)
graphs = data['graphs']

# Parse props.json
with open('props.json') as props_file:
    properties = json.load(props_file)

app = create_app()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = FullForm()

    if request.method == 'POST' and form.validate():
        props = []
        for prop in request.form:
            if prop != u'submit':
                props.append(request.form[prop])
        return redirect(url_for('search', encoded_props = encode_props(props)))

    form = populateForm()
    return render_template('home.html',form=form)
    
def populateForm():
    form = FullForm()

    # Remove old data
    while len(form.filters) > 0:
        form.filters.pop_entry()

    # Add data
    for prop in properties:
        new_entry = form.filters.append_entry()
        new_entry.label = prop['label']
        new_entry.choices = [(choice['name'], choice['label']) for choice in prop['choices']]
        new_entry.default = prop['default']
    return form

def encode_props(props):
    result = ''
    for i in range(len(props)):
        prop = props[i]
        for j in range(len(properties[i]['choices'])):
            if properties[i]['choices'][j]['name'] == prop:
                result += str(j)
                break

    return result

def decode_props(raw):
    props = []
    digits = [int(d) for d in str(raw)]
    # Check integrity
    if len(digits) != len(properties):
        return []
    for i in range(len(digits)):
        if len(properties[i]['choices']) > digits[i]: # Check integrity
            props.append(properties[i]['choices'][digits[i]]['name'])    
        else:
            return []
    return props

@app.route('/search/<encoded_props>')
def search(encoded_props):
    props = decode_props(encoded_props)
    if len(props) == 0:
        return render_template('404.html', error_msg='Unspecified filters'), 404
    else:
        return render_template('search.html', graphs=graphs, matches_filter=matches_filter, props=decode_props(encoded_props))

def matches_filter(graph, props):
    for prop in props:
        if prop != 'both' and not prop in graph['properties']:
            return False
    return True

@app.route('/graphs')
def graph_home():
    return render_template('list.html', graphs=graphs)

@app.route('/graphs/<graph_name>')
def graph(graph_name):
    graph = next((graph for graph in graphs if graph['name'] == graph_name), None)
    if graph != None:
        return render_template('graph.html', graph=graph)    
    else:
        return render_template('404.html', error_msg='No such graph exists!'), 404

@app.route('/random')
def get_random_graph():
	return redirect(url_for('graph', graph_name=random.choice(graphs)['name']))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error_msg='Page does not exist!'), 404
