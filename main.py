from flask import Flask, render_template,request
from products import fetch_products
from products import cur,delete_products,new_product
from datetime import datetime

app = Flask(__name__)

# Define a custom filter
@app.template_filter('strftime')
def format_datetime(value, format="%B %d, %Y"):
    return value.strftime(format)

@app.route("/")
def home():
    name = "William"
    return render_template("index.html", myname = name)

@app.route("/about")    
def about ():
    return "This is the about page"

@app.route("/contact")
def contact():
    return "This is the contact page"

@app.route("/products",methods=["GET","POST"])
def products():
    if request.method == "GET":
        cur.execute("SELECT * FROM products")    
        return render_template("products.html", prods = cur.fetchall())
    else:
        name = request.form ["pname"]
        buying_price = request.form["bp"]
        selling_price = request.form["sp"]
        stock_quantity = request.form["sq"]
        return "Product added!"        
                
@app.route("/sales")
def sales():
    cur.execute("SELECT sales.id,products.name,sales.quantity,sales.created_at FROM products INNER JOIN sales ON products.id = sales.pid")
    return render_template ("sales.html",sale = cur.fetchall())
    

if __name__ == "__main__":
    app.run(debug=True)
    