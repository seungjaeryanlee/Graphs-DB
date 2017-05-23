from flask import Flask, render_template
import json

# Parse data.json
with open('data.json') as data_file:    
    data = json.load(data_file)
graphs = data['graphs']

app = Flask(__name__)

@app.route('/')
def index():
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
        return '404 Not Found'
        #return render_template('404.html')