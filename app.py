from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to Graphs DB!'

@app.route('/graph')
def graph_home():
    return 'Here are list of graphs in our database.'

@app.route('/graph/<graphname>')
def graph(graphname):
    return render_template('graph.html', name=graphname.title(), description='Placeholder for description paragraph')