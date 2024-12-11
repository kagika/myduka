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
            if selling_price < buying_price:
                pass
            else:
                new_product(name,buying_price,selling_price,stock_quantity)
                redirect("/products")
        
                
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
    
@app.route("/dashboard")
def dashboard():
    sales_per_day_query = "SELECT SUM(products.selling_price * sales.quantity) as sales, sales.created_at FROM sales INNER JOIN products on sales.pid = products.id GROUP BY sales.created_at ORDER BY sales DESC;"
    cur.execute(sales_per_day_query)
    daily_sales = cur.fetchall()
    x = []
    y = []
    for i in daily_sales:
        x.append(i[1].strftime('%d %m %Y'))
        y.append(int(i[0]))      
    print(x)
    print(y)
    
    return render_template("dashboard.html",x=x,y=y)

@app.route("/dashboard2")
def dashboard2():
    query = "SELECT SUM(selling_price*quantity) AS total_sales, productS.name FROM products "\
            "INNER JOIN sales ON sales.pid = products.id GROUP BY products.name ORDER BY total_sales DESC;"
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    conn.close()
    x = [int(i[0]) for i in data]
    y = [i[1] for i in data]
    return render_template("dashboard2.html",x=x,y=y)


@app.route("/login",methods = ["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cur.execute(f"SELECT id FROM users WHERE email = '{email}'")
        row = cur.fetchone()
        if row == None:
            return "Invalid credentials"
    else:    
        return render_template("login.html")
        
        
@app.route("/register",methods = ["POST","GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        email = request.form["email"]
        password = request.form["password"]
        query = "insert into users(email,password) values('{}','{}')".format(email,password)
        cur.execute(query)
        conn.commit()
        return redirect("/dashboard")
    


# sales per product in a bar graph 

if __name__ == "__main__":
    app.run(debug=True)
    