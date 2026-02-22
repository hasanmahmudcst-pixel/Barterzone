from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='.')

# ডাটাবেস ফাইলের বদলে মেমোরি লিস্ট ব্যবহার (Vercel-এ এটিই সবচেয়ে নিরাপদ)
items_list = []
site_settings = {
    'about': 'আমাদের সম্পর্কে তথ্য এখানে লিখুন।',
    'refund': 'রিফান্ড পলিসি এখানে লিখুন।'
}

@app.route('/')
def home():
    return render_template('index.html', settings=site_settings)

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item = {
            'name': request.form.get('item_name'),
            'trxid': request.form.get('trx_id')
        }
        items_list.append(item)
        return redirect(url_for('home'))
    return render_template('add_item.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        site_settings['about'] = request.form.get('about_text')
        site_settings['refund'] = request.form.get('refund_text')
        return redirect(url_for('admin_panel'))
    return render_template('admin.html', items=items_list, settings=site_settings)

@app.route('/login')
def login():
    return render_template('admin_login.html')

# Vercel-এর জন্য হ্যান্ডলার
app = app

if __name__ == '__main__':
    app.run(debug=True)