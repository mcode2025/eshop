from flask import Flask, session, redirect, url_for, request, render_template_string, abort
from functools import wraps
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# CSS styles as string
CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; line-height: 1.6; padding: 20px; }
nav { background: #333; padding: 1rem; margin-bottom: 2rem; }
nav a { color: white; text-decoration: none; margin-right: 1rem; }
.product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 2rem; }
.product-card { border: 1px solid #ddd; padding: 1rem; border-radius: 8px; }
.product-card img { width: 100%; height: auto; }
.cart-item { display: flex; align-items: center; margin-bottom: 1rem; padding: 1rem; border: 1px solid #ddd; }
.cart-item img { width: 100px; margin-right: 1rem; }
input { padding: 0.5rem; margin-bottom: 1rem; width: 100%; }
button { background: #007bff; color: white; border: none; padding: 0.5rem 1rem; cursor: pointer; }
button:hover { background: #0056b3; }
@media (max-width: 600px) {
    .product-grid { grid-template-columns: 1fr; }
    .cart-item { flex-direction: column; text-align: center; }
}
"""

# Base template
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>E-Shop</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>""" + CSS + """</style>
</head>
<body>
    <nav>
        <a href="/">Home</a>
        <a href="/products">Products</a>
        <a href="/cart">Cart ({{session.get('cart', {})|length}})</a>
        <a href="/logout">Logout</a>
    </nav>
    {{content|safe}}
</body>
</html>
"""
# Replace the PRODUCTS dictionary with this updated version:

PRODUCTS = {
    1: {
        "name": "iPhone 14 Pro",
        "price": 999,
        "image": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-14-pro-finish-select-202209-6-7inch-deeppurple?wid=400",
        "description": "The iPhone 14 Pro features a 48MP camera system, Dynamic Island, and A16 Bionic chip for unprecedented performance and photography.",
        "specs": [
            "6.1-inch Super Retina XDR display",
            "48MP Main camera with ProRAW",
            "A16 Bionic chip",
            "Up to 1TB storage",
            "Emergency SOS via satellite"
        ],
        "stock": 15
    },
    3: {
        "name": "iPad Air",
        "price": 599,
        "image": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/ipad-air-select-wifi-blue-202203?wid=400",
        "description": "Powerful. Colorful. Wonderful. The iPad Air features the M1 chip for next-level performance and all-day battery life.",
        "specs": [
            "10.9-inch Liquid Retina display",
            "M1 chip with Neural Engine",
            "12MP Ultra Wide front camera",
            "USB-C connector",
            "Compatible with Apple Pencil (2nd gen)"
        ],
        "stock": 20
    },
    5: {
        "name": "MacBook Pro 14",
        "price": 1999,
        "image": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp14-spacegray-select-202301?wid=400",
        "description": "The most powerful MacBook Pro ever is here with the M2 Pro or M2 Max chip for unprecedented performance.",
        "specs": [
            "14.2-inch Liquid Retina XDR display",
            "Up to M2 Max with 12-core CPU",
            "Up to 96GB unified memory",
            "Up to 8TB storage",
            "Up to 18 hours battery life"
        ],
        "stock": 8
    },
    6: {
        "name": "AirPods Pro",
        "price": 249,
        "image": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MQD83?wid=400",
        "description": "AirPods Pro feature Active Noise Cancellation, Transparency mode, and Spatial Audio for an immersive listening experience.",
        "specs": [
            "Active Noise Cancellation",
            "Adaptive Transparency",
            "Personalized Spatial Audio",
            "Up to 6 hours listening time",
            "MagSafe Charging Case"
        ],
        "stock": 25
    },
    9: {
        "name": "Apple Watch Series 8",
        "price": 399,
        "image": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MKUQ3_VW_34FR+watch-45-alum-midnight-cell-8s_VW_34FR_WF_CO?wid=400",
        "description": "The Apple Watch Series 8 features advanced health sensors and safety features including Crash Detection and temperature sensing.",
        "specs": [
            "Always-On Retina display",
            "Temperature sensing",
            "Blood Oxygen monitoring",
            "ECG app capability",
            "Water resistant to 50m"
        ],
        "stock": 12
    }
}  


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin20250608':
            session['logged_in'] = True
            return redirect(url_for('products'))  # Changed from 'home' to 'products'
    return render_template_string(BASE_TEMPLATE, content="""
        <form method="post" style="max-width: 400px; margin: 0 auto;">
            <h2>Login</h2>
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    """)
@app.route('/')
@login_required
def home():
    return redirect(url_for('products'))  # Redirect root to products page

@app.route('/products')
@login_required
def products():
    products_html = "".join([f"""
        <div class="product-card">
            <img src="{p['image']}" alt="{p['name']}">
            <h3>{p['name']}</h3>
            <p>${p['price']}</p>
            <a href="/product/{pid}"><button>View Details</button></a>
        </div>
    """ for pid, p in PRODUCTS.items()])
    
    return render_template_string(BASE_TEMPLATE, content=f"""
        <h2>Our Products</h2>
        <div class="product-grid">{products_html}</div>
    """)
@app.route('/product/<int:pid>')
@login_required
def product(pid):
    if pid not in PRODUCTS:
        abort(404)
    p = PRODUCTS[pid]
    
    # Create specs HTML if specs exist
    specs_html = ""
    if "specs" in p:
        specs_html = """
            <div class="specs-section" style="margin: 2rem 0;">
                <h3>Specifications</h3>
                <ul style="list-style: none; padding: 0;">
                    {}
                </ul>
            </div>
        """.format("".join([f'<li style="margin: 0.5rem 0;">• {spec}</li>' for spec in p["specs"]]))
    
    # Modified stock status - only show if in stock
    stock_status = """
        <p style="color: #28a745; margin: 1rem 0;">
            In Stock ({} left)
        </p>
    """.format(p.get('stock', 0)) if p.get('stock', 0) > 0 else ""
    
    return render_template_string(BASE_TEMPLATE, content=f"""
        <div style="max-width: 800px; margin: 0 auto;">
            <div style="display: flex; flex-wrap: wrap; gap: 2rem;">
                <div style="flex: 1; min-width: 300px;">
                    <img src="{p['image']}" alt="{p['name']}" style="width: 100%; height: auto; border-radius: 8px;">
                </div>
                <div style="flex: 1; min-width: 300px;">
                    <h2>{p['name']}</h2>
                    <p style="font-size: 1.5rem; color: #007bff; margin: 1rem 0;">${p['price']}</p>
                    {stock_status}
                    <p style="margin: 1rem 0;">{p.get('description', '')}</p>
                    <form action="/add_to_cart/{pid}" method="post" style="margin: 2rem 0;">
                        <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
                            <input type="number" name="quantity" value="1" min="1" 
                                max="{p.get('stock', 5)}" style="width: 100px;"
                                required>
                            <button type="submit" style="flex-grow: 1;">Add to Cart</button>
                        </div>
                    </form>
                </div>
            </div>
            {specs_html}
        </div>
    """)
# Fix the add_to_cart function
@app.route('/add_to_cart/<int:pid>', methods=['POST'])
@login_required
def add_to_cart(pid):
    if pid not in PRODUCTS:
        abort(404)
    cart = session.get('cart', {})
    # Convert pid to string since session serialization converts keys to strings
    str_pid = str(pid)
    cart[str_pid] = cart.get(str_pid, 0) + 1
    session['cart'] = cart
    return redirect(url_for('cart'))
# Update the cart route function - look for existing cart function and replace with:

@app.route('/cart')
@login_required
def cart():
    cart = session.get('cart', {})
    total = sum(PRODUCTS[int(pid)]['price'] * qty for pid, qty in cart.items())
    items_html = "".join([f"""
        <div class="cart-item">
            <img src="{PRODUCTS[int(pid)]['image']}" alt="{PRODUCTS[int(pid)]['name']}">
            <div>
                <h3>{PRODUCTS[int(pid)]['name']}</h3>
                <p>Quantity: {qty}</p>
                <p>Price: ${PRODUCTS[int(pid)]['price'] * qty}</p>
                <form action="/remove_from_cart/{pid}" method="post" style="display: inline;">
                    <button type="submit">Remove</button>
                </form>
            </div>
        </div>
    """ for pid, qty in cart.items()])
    
    checkout_button = """
        <form action="/checkout" method="post" style="margin-top: 2rem;">
            <button type="submit" style="background-color: #28a745;">Proceed to Checkout</button>
        </form>
    """ if cart else ""
    
    return render_template_string(BASE_TEMPLATE, content=f"""
        <h2>Shopping Cart</h2>
        {items_html}
        <h3>Total: ${total}</h3>
        {checkout_button}
    """)
# Add these new routes after the cart function:

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('cart'))
    
    total = sum(PRODUCTS[int(pid)]['price'] * qty for pid, qty in cart.items())
    order_summary = "".join([f"""
        <div class="cart-item">
            <h3>{PRODUCTS[int(pid)]['name']}</h3>
            <p>Quantity: {qty}</p>
            <p>Price: ${PRODUCTS[int(pid)]['price'] * qty}</p>
        </div>
    """ for pid, qty in cart.items()])
    
    return render_template_string(BASE_TEMPLATE, content=f"""
        <div style="max-width: 800px; margin: 0 auto;">
            <h2>Checkout</h2>
            <div style="margin: 2rem 0;">
                <h3>Order Summary:</h3>
                {order_summary}
                <h3>Total Amount: ${total}</h3>
            </div>
            <form action="/confirm_order" method="post">
                <div style="margin-bottom: 1rem;">
                    <input type="text" name="name" placeholder="Full Name" required>
                    <input type="email" name="email" placeholder="Email Address" required>
                    <input type="text" name="address" placeholder="Shipping Address" required>
                    <input type="text" name="card" placeholder="Card Number" required>
                </div>
                <button type="submit" style="background-color: #28a745;">Confirm Order</button>
            </form>
        </div>
    """)

@app.route('/confirm_order', methods=['POST'])
@login_required
def confirm_order():
    if not session.get('cart'):
        return redirect(url_for('cart'))
    
    # Clear the cart after successful order
    session['cart'] = {}
    
    return render_template_string(BASE_TEMPLATE, content="""
        <div style="text-align: center; margin-top: 2rem;">
            <h2>Order Confirmed!</h2>
            <p>Thank you for your purchase. We'll send you an email with order details.</p>
            <a href="/products"><button style="margin-top: 1rem;">Continue Shopping</button></a>
        </div>
    """)

# Fix the remove_from_cart function
@app.route('/remove_from_cart/<int:pid>', methods=['POST'])
@login_required
def remove_from_cart(pid):
    cart = session.get('cart', {})
    str_pid = str(pid)  # Convert to string to match storage format
    if str_pid in cart:
        del cart[str_pid]
        session['cart'] = cart
    return redirect(url_for('cart'))
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template_string(BASE_TEMPLATE, content="<h2>Page Not Found</h2>"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template_string(BASE_TEMPLATE, content="<h2>Internal Server Error</h2>"), 500

if __name__ == '__main__':
    app.run(port=5103)