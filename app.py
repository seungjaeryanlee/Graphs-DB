from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import json
import random
from forms import FilterForm

def matches_filter(graph, props):
    for prop in props:
        if prop != 'both' and not prop in graph['properties']:
            return False
    return True

def encode_props(props):
    result = ''
    for prop in props:
        result += prop + '+'

    return result

def decode_props(raw):
    props = raw.split('+')[0:-1]
    return props

def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    return app

# Parse data.json
with open('data.json') as data_file:
    data = json.load(data_file)
graphs = data['graphs']

app = create_app()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = FilterForm(request.form)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('search', encoded_props = encode_props([form.planarity.data, form.directedness.data])))
    else:
        return render_template('home.html',form=form)

@app.route('/search/<encoded_props>')
def search(encoded_props):
    # FIXME: Use dictionray instead of list for props
    return render_template('search.html', graphs=graphs, matches_filter=matches_filter, props=decode_props(encoded_props))

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
