"""Simple admin panel"""
import os
from flask import Flask, render_template_string, request, redirect, url_for
from dotenv import load_dotenv
from .database import Session, User
from .parser import run as run_parser

load_dotenv()

app = Flask(__name__)

ADMIN_TEMPLATE = """
<!doctype html>
<title>Admin</title>
<h1>Users</h1>
<form method="get">
  <input name="tag" placeholder="Filter by tag">
  <button type="submit">Filter</button>
</form>
<table border="1">
<tr><th>ID</th><th>Name</th><th>Tags</th><th>Last Active</th></tr>
{% for u in users %}
<tr>
  <td>{{u.telegram_id}}</td>
  <td>{{u.first_name}}</td>
  <td>{{', '.join(t.name for t in u.tags)}}</td>
  <td>{{u.last_active}}</td>
</tr>
{% endfor %}
</table>
<a href="/parse">Run parser</a>
"""

@app.route('/')
def index():
    tag = request.args.get('tag')
    session = Session()
    q = session.query(User)
    if tag:
        q = q.join(User.tags).filter_by(name=tag)
    users = q.all()
    session.close()
    return render_template_string(ADMIN_TEMPLATE, users=users)

@app.route('/parse')
def parse():
    run_parser()
    return redirect(url_for('index'))


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
