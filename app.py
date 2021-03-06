from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)


def location(element):
    """
    str -> tuple
    Return the location of element
    """
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(timeout=10)
    location = geolocator.geocode(element)
    if location is not None:
        return (location.latitude, location.longitude)
    else:
        return None


def create_map(lst):
    """
    lst -> None
    Creates and saves the map to file
    """
    import folium
    map = folium.Map(tiles='Mapbox Control Room')
    layer = folium.FeatureGroup(name="Your friends around the world")
    for element in lst:
        print("Getting info about location...")
        if element[0] and element[1] is not None:
            try:
                icon_img = folium.features.CustomIcon("static/logo.png",
                                                      icon_size=(40, 40))
                layer.add_child(folium.Marker(
                    location=element[1], popup=element[0], icon=icon_img))
            except AttributeError:
                pass
    map.add_child(layer)
    map.add_child(folium.LayerControl())
    map.save("templates/Map.html")
    print("Saved")


@app.route('/')
def index():
    return render_template('input.html')


@app.route('/input', methods=["POST", "GET"])
def input():
    """
    get the username
    """
    if request.method == "POST":
        username = request.form['username']
        if username:
            return get_map(username)
    return render_template('input.html')


def get_map(account):
    """
    str->None
    """
    import urllib.request, urllib.parse, urllib.error
    import twurl
    import json
    import ssl

    # https://apps.twitter.com/
    # Create App and get the four strings, put them in hidden.py

    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    acct = account
    try:
        url = twurl.augment(TWITTER_URL,
                            {'screen_name': acct, 'count': '200'})
        connection = urllib.request.urlopen(url, context=ctx)
        data = connection.read().decode()
        js = json.loads(data)
        lst = []
        for u in js['users']:
            loc = location(u['location'])
            if loc:
                lst.append(tuple([u['screen_name'], loc]))
        create_map(lst)
        return redirect(url_for('show_map'))
    except urllib.error.HTTPError:
        return render_template("not_found.html")


@app.route('/map')
def show_map():
    return render_template('Map.html')


if __name__ == "__main__":
    app.run(debug=True)
