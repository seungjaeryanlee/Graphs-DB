from flask import Flask, render_template, redirect, url_for, request
import json
import random

# Parse data.json
with open('data.json') as data_file:    
    data = json.load(data_file)
graphs = data['graphs']

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('home.html', graphs=graphs)

    if request.method == 'POST':
        print(request.form.getlist('hello'))
        return render_template('home.html', graphs=graphs)

@app.route('/graphs')
def graph_home():
    return 'Here are list of graphs in our database.'

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
