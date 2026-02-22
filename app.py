from flask import Flask, render_template

app = Flask(__name__, template_folder='.')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/add')
def add_item():
    # এখানে ফাইলের নাম গিটহাবের সাথে হুবহু মিল থাকতে হবে
    return render_template('add_item.html')

if __name__ == '__main__':
    app.run()