from database import cur,conn

def fetch_products():
    cur.execute("SELECT*FROM products")
    products = cur.fetchall()
    print(products)
    return products

def sales():
    cur.execute("SELECT * FROM sales")    
    sales = cur.fetchall()
    print(sales)
    return sales

def new_product(nm,bp,sp,stock_quantity):
    cur.execute("INSERT INTO products(name,buying_price,selling_price,stock_quantity) VALUES (%s,%s,%s,%s);", (nm,bp,sp,stock_quantity))
    conn.commit()

def delete_products():
    cur.execute('DELETE FROM products WHERE id = 108;')
    conn.commit()



# product = input("Product name: ")
# buying_price = int(input("Buying price: "))
# selling_price = int(input("Selling price: "))
# stock_quantity = int(input("Stock quantity: "))

# new_product(product,buying_price,selling_price,stock_quantity)

delete_products()
