from flask import Flask, render_template
from products import fetch_products

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")    
def about ():
    return "This is the about page"

@app.route("/contact")
def contact():
    return "This is the contact page"

@app.route("/products")
def products():
    return fetch_products()
    
    
    

if __name__ == "__main__":
    app.run(debug=True)
    