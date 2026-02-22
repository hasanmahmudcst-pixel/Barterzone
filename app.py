from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "barterzone_secret_key_123"  # এটি সেশন ম্যানেজ করার জন্য জরুরি

# ডেমো ডেটা (প্রাথমিক অবস্থায় পণ্য দেখানোর জন্য)
items = [
    {
        "id": 1,
        "name": "Gaming Console",
        "desc": "Used for 1 year, looks brand new with two controllers.",
        "exchange": "Laptop or iPad",
        "owner": "Hasan"
    },
    {
        "id": 2,
        "name": "Bicycle",
        "desc": "Mountain bike, well maintained, 21 gears.",
        "exchange": "Smart Watch or Smartphone",
        "owner": "Rifat"
    },
    {
        "id": 3,
        "name": "DSLR Camera",
        "desc": "Canon EOS 700D with 18-55mm lens.",
        "exchange": "Electric Guitar",
        "owner": "Adnan"
    }
]

@app.route('/')
def home():
    search_query = request.args.get('search')
    if search_query:
        # সার্চ বক্সে কিছু লিখলে তা এখানে ফিল্টার হবে
        filtered_items = [i for i in items if search_query.lower() in i['name'].lower()]
        return render_template('index.html', items=filtered_items)
    return render_template('index.html', items=items)

@app.route('/auth')
def auth():
    # ডেমো লগইন সিস্টেম: ক্লিক করলেই ইউজার হিসেবে লগইন হয়ে যাবে
    session['user'] = "Hasan Mahmud"
    return redirect(url_for('home'))

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if 'user' not in session:
        return redirect(url_for('auth'))
    
    if request.method == 'POST':
        # নতুন পণ্য যোগ করার লজিক
        new_item = {
            "id": len(items) + 1,
            "name": request.form.get('name'),
            "desc": request.form.get('desc'),
            "exchange": request.form.get('exchange'),
            "owner": session['user']
        }
        items.append(new_item)
        return redirect(url_for('home'))
    
    return render_template('add_item.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# Vercel-এ রান করার জন্য এটি প্রয়োজন
if __name__ == "__main__":
    app.run(debug=True)