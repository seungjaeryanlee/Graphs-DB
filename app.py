from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import json
import random
from forms import FullForm, RadioField

# Parse data.json and props.json
with open('data.json') as data_file:
    graphs = json.load(data_file)
with open('props.json') as props_file:
    properties = json.load(props_file)

def create_app():
    """
    Creates flask_bootstrap app.
    """
    app = Flask(__name__)
    Bootstrap(app)
    return app

app = create_app()

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Renders the home page if it is a GET request. Redirects to search page if 
    a form was submitted
    """
    form = FullForm()

    if request.method == 'POST' and form.validate():
        # Append properties in the same order as props.json
        props = []
        for i in range(len(properties)):
            props.append(request.form['filters-'+str(i)])

        return redirect(url_for('search', encoded_props = encode_props(props)))

    form = populateForm()
    return render_template('home.html',form=form)
    
def populateForm():
    """
    Returns a form populated according to properties
    """
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
    """
    Encodes props array to digits and returns them. Assumes that each property 
    has at most 10 choices
    """
    result = ''
    for i in range(len(props)):
        prop = props[i]
        for j in range(len(properties[i]['choices'])):
            if properties[i]['choices'][j]['name'] == prop:
                result += str(j)
                break

    return result

def decode_props(raw):
    """
    Decodes props array from digits and returns it. Returns empty array if the
    digits have incorrect format
    """
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
    """
    Renders the search page if the digits are correct. If not, renders a 404
    page.
    """
    props = decode_props(encoded_props)
    if len(props) == 0:
        return render_template('404.html', error_msg='Unspecified filters'), 404
    else:
        return render_template('search.html', graphs=graphs, matches_filter=matches_filter, props=decode_props(encoded_props))

def matches_filter(graph, props):
    """
    Returns True if a given graph matches all the given props. Returns False
    if not.
    """
    for prop in props:
        if prop != 'all' and not prop in graph['properties']:
            return False
    return True

@app.route('/graphs')
def graph_home():
    """
    Renders a page with a list of all the graphs
    """
    return render_template('list.html', graphs=graphs)

@app.route('/graphs/<graph_name>')
def graph(graph_name):
    """
    Renders a graph page if the graph with the given graph_name exists. Renders 
    a 404 page if not.
    """
    graph = next((graph for graph in graphs if graph['name'] == graph_name), None)
    if graph != None:
        return render_template('graph.html', graph=graph)    
    else:
        return render_template('404.html', error_msg='No such graph exists!'), 404

@app.route('/random')
def redirect_random_graph():
    """
    Redirects to a random graph page.
    """
    return redirect(url_for('graph', graph_name=random.choice(graphs)['name']))

@app.errorhandler(404)
def page_not_found(e):
    """
    Renders a 404 page.
    """
    return render_template('404.html', error_msg='Page does not exist!'), 404
