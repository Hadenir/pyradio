from radio import *
from controls import *
from flask import *

app = Flask(__name__)
radio = Radio()
controls = Controls(radio)

@app.route('/')
def index():
    return render_template('index.html',
        stations = radio.stations,
        current_station_id = radio.current_station_id,
        current_station = radio.current_station(),
        playing = radio.state == Radio.State.PLAYING)

@app.route('/add-station', methods=['POST'])
def add_station():
    station_name = request.form['station-name']
    station_url = request.form['station-url']
    station = RadioStation(station_name, station_url)

    radio.add_station(station)
    return redirect(request.referrer)

@app.route('/station/<int:id>', methods=['GET'])
def get_station(id: int):
    station = radio.get_station(id)
    return {
        'station_name': station.name,
        'station_url': station.url,
    }

@app.route('/edit-station/<int:id>', methods=['POST'])
def edit_station(id: int):
    station_name = request.form['station-name']
    station_url = request.form['station-url']
    station = RadioStation(station_name, station_url)

    radio.edit_station(id, station)
    return redirect(request.referrer)

@app.route('/remove-station/<int:id>',)
def remove_station(id: int):
    radio.remove_station(id)
    return redirect(request.referrer)

@app.route('/select-station/<int:id>')
def select_station(id: int):
    radio.select_station(id)
    return redirect(request.referrer)

@app.route('/next-station')
def next_station():
    radio.next_station()
    return redirect(request.referrer)

@app.route('/prev-station')
def prev_station():
    radio.prev_station()
    return redirect(request.referrer)

@app.route('/play')
def play():
    radio.play()
    return redirect(request.referrer)

@app.route('/pause')
def pause():
    radio.pause()
    return redirect(request.referrer)

@app.route('/set-volume/<int:value>')
def set_volume(value: int):
    radio.set_volume(value)
    return redirect(request.referrer)

@app.route('/get-volume', methods=['GET'])
def get_volume():
    return {
        "volume": radio.get_volume()
    }


app.run(host='0.0.0.0', port=8080, debug=True)
