from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = "barter_secret_key_99"

# MongoDB Connection
MONGO_URI = "mongodb+srv://adminberterzone:Habiba19892@cluster0.pg3xfac.mongodb.net/berterzone_db?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['berterzone_db']
products_collection = db['products']
settings_collection = db['settings'] # About ও Refund Policy এর জন্য

@app.route('/')
def index():
    products = list(products_collection.find({"status": "Approved"}))
    # ডাটাবেস থেকে সেটিংস আনা, না থাকলে ডিফল্ট লেখা দেখানো
    site_settings = settings_collection.find_one() or {
        "about": "আমাদের সম্পর্কে তথ্য এখানে আসবে।",
        "refund": "রিফান্ড পলিসি এখানে আসবে।"
    }
    return render_template('index.html', products=products, settings=site_settings)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == "Habiba19892":
            session['admin'] = True
            return redirect(url_for('admin'))
        flash("ভুল পাসওয়ার্ড!")
    return render_template('auth.html')

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        trx_id = request.form.get('trx_id')
        if not trx_id:
            flash("Transaction ID প্রদান করা বাধ্যতামূলক।")
            return redirect(url_for('add_item'))
            
        new_product = {
            "name": request.form.get('name'),
            "price": request.form.get('price'),
            "trx_id": trx_id,
            "status": "Pending"
        }
        products_collection.insert_one(new_product)
        flash("আইটেম সাবমিট হয়েছে! পেমেন্ট ভেরিফাই হলে এটি হোমপেজে দেখাবে।")
        return redirect(url_for('index'))
    return render_template('add_item.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Admin About Us এবং Refund Policy আপডেট করার লজিক
        settings_collection.update_one(
            {}, 
            {"$set": {
                "about": request.form.get('about'),
                "refund": request.form.get('refund')
            }}, 
            upsert=True
        )
        flash("সেটিংস আপডেট হয়েছে!")
        return redirect(url_for('admin'))

    products = list(products_collection.find())
    current_settings = settings_collection.find_one() or {"about": "", "refund": ""}
    return render_template('admin.html', products=products, settings=current_settings)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)