from flask import Flask, render_template

bike_garage = Flask(__name__)


@bike_garage.route("/")
@bike_garage.route("/index.html")
def index():
    return render_template("index.html")


@bike_garage.route('/index.html/<int:bike_num>')
def bike(bike_num=1):
    #  ... read the bike data here based on the bike passed into the route from "bike selector" dropdown ...
    return render_template('index.html', bike_data=bike_num)


@bike_garage.route("/usage")
def usage():
    ride_data = {
        "Date": "%d. %m. %Y",
        "Ride Type": "casual/high intensity/bikepark/jumps",
        "Distance": "XXXkm/mil",
        "Duration": "%H:%M",
        "Elevation Gain": "XXXkm/ft",
        "Strava link": "link in form of map (provided by strava)"
    }
    return render_template("usage.html",
                           ride_data=ride_data)


@bike_garage.route("/components")
def components():
    return render_template("components.html")


if __name__ == "__main__":
    bike_garage.run(debug=True)
