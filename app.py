from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

app = Flask(__name__, template_folder='.')
app.secret_key = "barterzone_secret_key" # সেশন নিরাপত্তার জন্য

# অ্যাডমিন ক্রেডেনশিয়াল (প্রয়োজনে এখান থেকে পরিবর্তন করুন)
ADMIN_USERNAME = "admin@berterzone.com"
ADMIN_PASSWORD = "Habiba@19892"

items_list = []
site_settings = {
    'about': 'আমাদের সম্পর্কে তথ্য এখানে লিখুন।',
    'refund': 'রিফান্ড পলিসি এখানে লিখুন।'
}

# অ্যাডমিন প্যানেল সুরক্ষিত করার ডেকোরেটর
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html', settings=site_settings)

@app.route('/auth')
def auth():
    return render_template('auth.html')

# পণ্য যোগ করার রুট (আপনার নতুন HTML ডিজাইনের সাথে মিল রেখে)
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item = {
            'name': request.form.get('item_name'),
            'email': request.form.get('user_email'), # ইমেইল ফিল্ড যুক্ত করা হয়েছে
            'trxid': request.form.get('trx_id')
        }
        items_list.append(item)
        return redirect(url_for('home'))
    return render_template('add_item.html')

# লগইন রুট
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')
        if user == ADMIN_USERNAME and pwd == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            error = 'ভুল ইউজারনেম অথবা পাসওয়ার্ড!'
    return render_template('admin_login.html', error=error)

# অ্যাডমিন প্যানেল রুট (আপনার নতুন টেবিল ডিজাইনের সাথে মিল রেখে)
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if request.method == 'POST':
        site_settings['about'] = request.form.get('about_text')
        site_settings['refund'] = request.form.get('refund_text')
        return redirect(url_for('admin_panel'))
    return render_template('admin.html', items=items_list, settings=site_settings)

# লগআউট রুট
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

app = app # Vercel-এর জন্য

if __name__ == '__main__':
    app.run(debug=True)