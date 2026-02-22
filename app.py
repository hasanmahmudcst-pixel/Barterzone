from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query

app = Flask(__name__, template_folder='.')
db = TinyDB('db.json') # এখানে সব তথ্য সেভ হবে

# প্রাথমিক কিছু তথ্য ডাটাবেসে সেট করা (যদি খালি থাকে)
if not db.all():
    db.insert({'type': 'settings', 'about': 'আমাদের সম্পর্কে এখানে লিখুন', 'refund': 'রিফান্ড পলিসি এখানে লিখুন'})

@app.route('/')
def home():
    settings = db.search(Query().type == 'settings')[0]
    return render_template('index.html', settings=settings)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item = {
            'type': 'item',
            'name': request.form.get('item_name'),
            'trxid': request.form.get('trx_id')
        }
        db.insert(item)
        return "পণ্য সফলভাবে জমা হয়েছে!"
    return render_template('add_item.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        # অ্যাডমিন যখন About বা Refund আপডেট করবে
        new_about = request.form.get('about_text')
        new_refund = request.form.get('refund_text')
        db.update({'about': new_about, 'refund': new_refund}, Query().type == 'settings')
        return redirect(url_for('admin_panel'))
    
    items = db.search(Query().type == 'item')
    settings = db.search(Query().type == 'settings')[0]
    return render_template('admin.html', items=items, settings=settings)

if __name__ == '__main__':
    app.run()