from flask import Flask, render_template

bike_garage = Flask(__name__)


@bike_garage.route("/")
def home():
    return render_template("usage.html")


@bike_garage.route("/usage")
def usage():
    return render_template("usage.html")


@bike_garage.route("/components")
def components():
    return render_template("components.html")


if __name__ == "__main__":
    bike_garage.run(debug=True)
