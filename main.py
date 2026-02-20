@app.route("/dashboard")
def dashboard():
    conn = connect()

    products = pd.read_sql_query("SELECT COUNT(*) as total FROM products", conn).iloc[0]["total"]
    inventory = pd.read_sql_query("SELECT SUM(quantity) as total FROM inventory", conn).iloc[0]["total"]

    low_stock = pd.read_sql_query("""
        SELECT p.name, i.quantity
        FROM inventory i
        JOIN products p ON p.id=i.product_id
        WHERE i.quantity < 10
    """, conn)

    conn.close()

    return f"""
    <h1>Inventory Dashboard</h1>
    <h3>Total Products: {products}</h3>
    <h3>Total Stock Units: {inventory}</h3>

    <h3>Low Stock Alerts</h3>
    {low_stock.to_html(index=False)}

    <hr>
    <a href='/products'>Manage Products</a><br>
    <a href='/inventory'>Manage Inventory</a><br>
    <a href='/export'>Export Report</a>
    """

