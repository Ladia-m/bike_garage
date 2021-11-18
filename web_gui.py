from collections import namedtuple
from flask import Flask, render_template, request

bike_garage = Flask(__name__)

BikeDescriptor = namedtuple("BikeDescriptor", "name color size components")
Point = namedtuple("Point", "x y")
Point(x=2, y=4)
all_bikes = {
    "1": BikeDescriptor(name='Sean', color='Red', size='22', components={'wheel_size': 22, 'frame_size': 222})
}


@bike_garage.route("/")
@bike_garage.route("/index.html")
def index(bike_num=None):
    return render_template("index.html",
                           bike_data=bike_num)


@bike_garage.route("/usage/")
def usage():
    chart_data = [10, 41, 35, 51, 49, 62, 69, 2, 148]
    chart_data2 = [10, 41, 52, 1, 49, 62, 69, 91, 148]
    chart_xseries = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']
    ride_data = {
        "Date": "%d. %m. %Y",
        "Ride Type": "casual/high intensity/bikepark/jumps",
        "Distance": "XXXkm/mil",
        "Duration": "%H:%M",
        "Elevation Gain": "XXXkm/ft",
        "Strava link": "link in form of map (provided by strava)"
    }
    return render_template(
        "usage.html",
        chart_data=chart_data,
        chart_data2=chart_data2,
        chart_xseries=chart_xseries,
        ride_data=ride_data
    )


@bike_garage.route("/components/")
def components():
    bike_num = request.args.get('bike_num')
    if not bike_num or bike_num not in all_bikes:
        return render_template("components.html")
    return render_template("components.html", component_data=all_bikes[bike_num].components)


@bike_garage.route("/setup/")
def setup():
    return render_template("setup.html")


@bike_garage.route("/wishlist/")
def wishlist():
    return render_template("wishlist.html")
