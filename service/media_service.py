import vlc, time

class MediaService():
    def __init__(self):
        self.player = vlc.MediaPlayer()

    def set_audio(self, url):
        media = vlc.Media(url)
        self.player.set_media(media)

    def play_audio(self, timestamp=0, length=1, pos=0):
        """Takes timestamp and length (if provided) in ms, 
        and sets player position based off their values
        
        .. note:: If pos is not 0, use pos to set current position"""
        if pos == 0: pos = timestamp / length
        self.player.play()
        self.player.set_position(pos)

    def get_curr_timestamp(self):
        return self.player.get_time()
    
    def pause_audio(self):
        self.player.pause()
    
    def set_pos(self, pos):
        self.player.set_position(pos)

    def skip_time(self, time=15000):
        new_time = self.get_curr_timestamp() + time
        if new_time >= self.player.get_length():
            self.player.set_position(1)
            self.player.pause()
        elif new_time <= 0:
            self.player.set_position(0)
        else:
            pos = new_time / self.player.get_length()
            self.player.set_position(pos)

# player = vlc.MediaPlayer('https://traffic.libsyn.com/secure/friendsatthetable/fatt_intro_2020.mp3?dest-id=550849')

media_service = MediaService()
media_service.set_audio('https://traffic.libsyn.com/secure/friendsatthetable/fatt_intro_2020.mp3?dest-id=550849')
media_service.play_audio(pos=0.2)
time.sleep(1)
# timestamp = media_service.get_curr_timestamp()



time.sleep(60)