from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = "barter_secret_key_123"

# MongoDB Connection
MONGO_URI = "mongodb+srv://adminberterzone:Habiba19892@cluster0.pg3xfac.mongodb.net/berterzone_db?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['berterzone_db']
products_collection = db['products']
settings_collection = db['settings']

@app.route('/')
def index():
    try:
        products = list(products_collection.find())
        # সেটিংস চেক করা হচ্ছে যাতে 'settings is undefined' এরর না আসে
        site_settings = settings_collection.find_one()
        if not site_settings:
            site_settings = {
                "about": "আমাদের সম্পর্কে তথ্য যোগ করতে অ্যাডমিন প্যানেলে যান।",
                "refund": "রিফান্ড পলিসি এখনো সেট করা হয়নি।"
            }
        return render_template('index.html', products=products, settings=site_settings)
    except Exception as e:
        return f"Database error: {str(e)}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == "Habiba19892":
            session['admin'] = True
            return redirect(url_for('admin'))
        flash("ভুল পাসওয়ার্ড!")
    return render_template('auth.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # About ও Refund আপডেট করার লজিক
        about_text = request.form.get('about')
        refund_text = request.form.get('refund')
        
        settings_collection.update_one(
            {}, 
            {"$set": {"about": about_text, "refund": refund_text}}, 
            upsert=True
        )
        flash("তথ্য সফলভাবে আপডেট করা হয়েছে!")
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