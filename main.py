from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = "website_secret_key"

users = {}

@app.route('/')
def index():
    return '''
        <h1>Welcome!</h1>
        <a href="/register">Register</a><br>
        <a href="/login">Login</a>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            error = "User Exists!"
        else:
            users[username] = password
            return redirect(url_for('login'))
    return render_template_string('''
        <form method="post">
            Username: <input name="username" required><br>
            Password: <input type="password" name="password" required><br>
            <button>Register</button>
        </form>
        {% if error %}<p style="color:red">{{error}}</p>{% endif %}
    ''', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('welcome'))
        else:
            error = "Username or Password incorrect."
    return render_template_string('''
        <form method="post">
            Username: <input name="username" required><br>
            Password: <input type="password" name="password" required><br>
            <button>Login</button>
        </form>
        {% if error %}<p style="color:red">{{error}}</p>{% endif %}
    ''', error=error)

@app.route('/welcome')
def welcome():
    if 'user' not in session:
        return redirect(url_for('login'))
    return f"Welcome, {session['user']}<br><a href='/logout'>Logout</a>"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
