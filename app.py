from flask import Flask, render_template
from flask_flatpages import FlatPages, pygments_style_defs
import json


DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'
PORTFOLIO_FILE = 'portfolio/projects.json'


app = Flask(__name__)
flatpages = FlatPages(app)
app.config.from_object(__name__)


@app.route('/')
def index():
	posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
	posts.sort(key=lambda i: i['date'], reverse=True)
	return render_template('index.html', posts=posts, bigheader=True)


@app.route('/blog/<post_name>/')
def post(post_name):
	path = '{}/{}'.format(POST_DIR, post_name)
	post = flatpages.get_or_404(path)
	return render_template('post.html', post=post)


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/portfolio')
def portfolio():
	path = '{}/{}'.format(FLATPAGES_ROOT, PORTFOLIO_FILE)
	data = None
	with open(path, 'r', encoding='utf-8') as f:
		data = json.load(f)
	projects = data['projects']
	return render_template('portfolio.html', projects=projects)


@app.route('/pygments.css')
def pygments_css():
	return pygments_style_defs('monokai'), 200, {'Content-Type': 'text/css'}


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=False)