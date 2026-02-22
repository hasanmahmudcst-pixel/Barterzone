from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Barterzone is Live! Your setup is successful."

if __name__ == "__main__":
    app.run(debug=True)