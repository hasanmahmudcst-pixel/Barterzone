from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='.')

# ডাটা জমা রাখার লিস্ট
items_list = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # পেমেন্ট আইডি সহ ডাটা নেওয়া
        new_item = {
            'name': request.form.get('item_name'),
            'category': request.form.get('category'),
            'description': request.form.get('description'),
            'exchange': request.form.get('exchange_with'),
            'trxid': request.form.get('trx_id') # ট্রানজেকশন আইডি
        }
        items_list.append(new_item)
        return redirect(url_for('admin_panel'))
    return render_template('add_item.html')

@app.route('/admin')
def admin_panel():
    return render_template('admin.html', items=items_list)

if __name__ == '__main__':
    app.run()