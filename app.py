from flask import Flask, render_template

# template_folder='.' কারণ আপনার সব HTML ফাইল মেইন ডিরেক্টরিতে আছে
app = Flask(__name__, template_folder='.')

# ১. হোম পেজ (Index)
@app.route('/')
def home():
    return render_template('index.html')

# ২. লগইন পেজ (Admin Login)
@app.route('/login')
def login():
    return render_template('admin_login.html')

# ৩. অথেনটিকেশন পেজ (Auth)
@app.route('/auth')
def auth():
    return render_template('auth.html')

# ৪. অ্যাডমিন প্যানেল (Admin)
@app.route('/admin')
def admin():
    return render_template('admin.html')

# ৫. আইটেম যোগ করার পেজ (Add Item)
@app.route('/add')
def add_item():
    return render_template('add_item.html')

if __name__ == '__main__':
    app.run()