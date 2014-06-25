from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2


app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site""" 
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""

    melon_dict = {}
    total_sum = 0

    for id in session.get("cart",{}):
        melon = model.get_melon_by_id(id)
        melon_dict[melon] = session["cart"][id]
        total_sum += melon.price*melon_dict[melon]

    return render_template("cart.html",
                              cart = melon_dict,
                              total = "$%.2f" % total_sum)

    
@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.
    
    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """

    id = str(id)

    cart_exists = session.get("cart")


    if cart_exists:
        session["cart"][id] = session["cart"].get(id, 0) + 1
        print session["cart"]
        flash("Successfully added to cart!")
    else:
        session["cart"] = {}
        session["cart"][id] = 1
        flash("Successfully added to cart!")

    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""

    email = request.form.get("email")
    password = request.form.get("password")

    customer = model.get_customer_by_email(email)

    if customer and password == customer.password:
        session["customer"] = [str(customer.first_name), str(customer.last_name), str(customer.email)]
        flash ("Welcome %s!" % str(customer.first_name))
        return redirect("/melons")
    elif customer and password != customer.password:
        flash ("Incorrect password.")
        return redirect("/login")
    else:
        flash ("Please register with Ubermelon")
        return redirect("/login")


@app.route("/logout")
def logout():
    session.clear()

    return redirect("/login")

@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

@app.route("/register", methods=["GET"])
def show_register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def process_register():

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    if model.register_customer(first_name, last_name, email, password):
        session["customer"] = [first_name,last_name, email]
        flash ("Welcome %s!" % first_name)
        flash("Successfully registered!")
        return redirect("/melons")
    else:
        flash("Problem with registration")
        return redirect("/register")


@app.route("/update", methods=["POST"])
def update():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    for melon_id in session["cart"].keys():
        if request.form.get(melon_id) != '':
            session["cart"][melon_id] = int(request.form.get(melon_id))
    print session["cart"]

    return redirect("/cart")

if __name__ == "__main__":
    app.run(debug=True)
