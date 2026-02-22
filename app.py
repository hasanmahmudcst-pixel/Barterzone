from flask import Flask, render_template

app = Flask(__name__)

# হোম পেজ - যেখানে ইউজাররা আপনার সাইট দেখবে
@app.route('/')
def home():
    return render_template('index.html')

# পণ্য যোগ করার পেজ (আপনার templates ফোল্ডারে add_item.html আছে)
@app.route('/add')
def add_item():
    return render_template('add_item.html')

# অ্যাডমিন প্যানেল (আপনার templates ফোল্ডারে admin.html আছে)
@app.route('/admin')
def admin():
    return render_template('admin.html')

# এটি Vercel-এর জন্য প্রয়োজন
if __name__ == '__main__':
    app.run(debug=True)