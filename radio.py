from enum import Enum
import vlc

class RadioStation:
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

class Radio:
    class State(Enum):
        PAUSED = 0
        PLAYING = 1

    stations = []
    state = State.PAUSED

    def __init__(self):
        self.vlc_instance: vlc.Instance = vlc.Instance()
        self.player: vlc.MediaPlayer = self.vlc_instance.media_player_new()
        self.player.audio_set_volume(50)

        self.stations.append(RadioStation('Radio Koszalin', 'http://91.232.4.33:9680/stream'))
        self.stations.append(RadioStation('RMF Maxxx', 'http://195.150.20.4/rmf_maxxx_waw'))
        self.stations.append(RadioStation('Majestic Jukebox Radio', 'http://uk3.internet-radio.com:8405/stream'))
        self.stations.append(RadioStation('Dance UK Radio', 'http://uk2.internet-radio.com:8024/stream'))
        self.stations.append(RadioStation('Classic Rock Florida', 'http://uk3.internet-radio.com:8405/stream'))
        self.stations.append(RadioStation('BBC Radio 1', 'http://stream.live.vc.bbcmedia.co.uk/bbc_radio_one'))
        self.stations.append(RadioStation('BBC Radio 1 Extra', 'http://stream.live.vc.bbcmedia.co.uk/bbc_1xtra'))

        self.current_station_id = -1

    def add_station(self, station: RadioStation):
        self.stations.append(station)

    def get_station(self, station_id: int):
        return self.stations[station_id]

    def edit_station(self, station_id: int, station: RadioStation):
        self.stations[station_id] = station

    def remove_station(self, station_id: int):
        del self.stations[station_id]

        if self.current_station_id == station_id:
            self.select_station(None)
        elif self.current_station_id > station_id:
            self.current_station_id -= 1

    def select_station(self, station_id: int):
        if station_id is None:
            self.pause()
            self.current_station_id = -1
            return

        if station_id >= len(self.stations):
            station_id = 0
        elif station_id < 0:
            station_id = len(self.stations) - 1

        station = self.stations[station_id]

        self.current_station_id = station_id
        self.player.set_media(self.vlc_instance.media_new_location(station.url))
        if self.state == Radio.State.PLAYING:
            self.player.play()

    def next_station(self):
        self.select_station(self.current_station_id + 1)

    def prev_station(self):
        self.select_station(self.current_station_id - 1)

    def current_station(self):
        if self.current_station_id < 0 or self.current_station_id >= len(self.stations):
            return None
        return self.stations[self.current_station_id]

    def play(self):
        if self.current_station_id < 0 or self.current_station_id >= len(self.stations):
            return

        self.player.play()
        self.state = Radio.State.PLAYING

    def pause(self):
        self.player.pause()
        self.state = Radio.State.PAUSED

    def play_pause(self):
        if self.state == Radio.State.PLAYING:
            self.pause()
        else:
            self.play()

    def set_volume(self, percent: int):
        volume = max(0, min(100, percent))
        self.player.audio_set_volume(volume)

    def get_volume(self):
        return self.player.audio_get_volume()
