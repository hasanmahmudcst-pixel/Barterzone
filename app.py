from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import os

app = Flask(__name__, template_folder='.')
app.secret_key = "barterzone_super_secret_key" # এটি সেশন সুরক্ষার জন্য

# অ্যাডমিন লগইন তথ্য
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123" # আপনি এখানে নিজের পছন্দমতো পাসওয়ার্ড সেট করুন

# সাময়িক ডেটা স্টোরেজ (Vercel-এর জন্য নিরাপদ)
items_list = []
site_settings = {
    'about': 'আমাদের সম্পর্কে তথ্য এখানে লিখুন।',
    'refund': 'রিফান্ড পলিসি এখানে লিখুন।'
}

# নিরাপত্তা ডেকোরেটর: লগইন ছাড়া অ্যাডমিন পেজে যাওয়া যাবে না
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- রুটস (Routes) ---

@app.route('/')
def home():
    return render_template('index.html', settings=site_settings)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # পাসওয়ার্ড চেক করা হচ্ছে
        user = request.form.get('username')
        pwd = request.form.get('password')
        
        if user == ADMIN_USERNAME and pwd == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            error = 'ভুল ইউজারনেম অথবা পাসওয়ার্ড!'
            
    return render_template('admin_login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/admin', methods=['GET', 'POST'])
@login_required # এখানে পাসওয়ার্ড নিরাপত্তা কাজ করবে
def admin_panel():
    if request.method == 'POST':
        # অ্যাডমিন থেকে সাইট আপডেট
        site_settings['about'] = request.form.get('about_text')
        site_settings['refund'] = request.form.get('refund_text')
        return redirect(url_for('admin_panel'))
    
    return render_template('admin.html', items=items_list, settings=site_settings)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # ইউজার থেকে ডেটা নেওয়া
        new_item = {
            'name': request.form.get('item_name'),
            'category': request.form.get('category'),
            'trxid': request.form.get('trx_id')
        }
        items_list.append(new_item)
        return redirect(url_for('home'))
    return render_template('add_item.html')

@app.route('/auth')
def auth():
    return render_template('auth.html')

# Vercel-এর জন্য হ্যান্ডলার
app = app

if __name__ == '__main__':
    app.run(debug=True)