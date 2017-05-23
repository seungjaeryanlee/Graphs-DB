from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/graph')
def graph_home():
    return 'Here are list of graphs'

@app.route('/graph/<graphname>')
def graph(graphname):
    return render_template('graph.html', name=graphname, description='Placeholder for description paragraph')