from flask import Flask, render_template

app = Flask(__name__, template_folder='.')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/auth')
def auth():
    return render_template('auth.html')

# নিশ্চিত করুন গিটহাবে ফাইলের নাম add_item.html ই আছে
@app.route('/add')
def add_item():
    return render_template('add_item.html')

# নিশ্চিত করুন গিটহাবে ফাইলের নাম admin.html ই আছে
@app.route('/admin')
def admin():
    return render_template('admin.html')

# নিশ্চিত করুন গিটহাবে ফাইলের নাম admin_login.html ই আছে
@app.route('/login')
def login():
    return render_template('admin_login.html')

if __name__ == '__main__':
    app.run()