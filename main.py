from flask import Flask, render_template,request,redirect
from products import fetch_products
from products import cur,new_product,conn
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
        cur.execute("SELECT * FROM products order by id desc")    
        prods = cur.fetchall()
        print(prods)
        return render_template("products.html",prods = prods)
    else:
            name = request.form ["pname"]
            buying_price = request.form["bp"]
            selling_price = request.form["sp"]
            stock_quantity = request.form["sq"]
            if selling_price > buying_price:
                new_product(name,buying_price,selling_price,stock_quantity)
                return redirect("/products")
            else:
                return "A loss will be realised and cannot be put into the database"
            
        
                
@app.route("/sales", methods = ["GET","POST"])
def sales():
    if request.method == "POST":
        product_id = request.form["pid"]
        product_quantity = request.form["product_quantity"]
        print(product_id,product_quantity)
        query = f"INSERT INTO sales (pid,quantity,created_at) VALUES ({product_id},{product_quantity},now())"
        cur.execute(query)
        conn.commit()
        return redirect("/sales")
    else:
        cur.execute("select * from products")
        products = cur.fetchall()
        cur.execute("SELECT sales.id,products.name,sales.quantity,sales.created_at FROM products INNER JOIN sales ON products.id = sales.pid")
        sale = cur.fetchall()
        return render_template ("sales.html",sales = sale,products = products )
    
        

if __name__ == "__main__":
    app.run(debug=True)
    