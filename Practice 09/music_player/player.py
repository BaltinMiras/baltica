from pathlib import Path
import pygame


class MusicPlayer:
    def __init__(self, music_directory):
        self.music_directory = Path(music_directory)
        self.music_directory.mkdir(parents=True, exist_ok=True)
        self.tracks = sorted(
            path for path in self.music_directory.rglob("*")
            if path.is_file() and path.suffix.lower() in {".mp3", ".wav", ".ogg"}
        )
        self.current_index = 0
        self.playing = False
        pygame.mixer.init()

    @property
    def current_track(self):
        if not self.tracks:
            return None
        return self.tracks[self.current_index]

    def play(self):
        if self.current_track is None:
            return
        pygame.mixer.music.load(str(self.current_track))
        pygame.mixer.music.play()
        self.playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    def next_track(self):
        if not self.tracks:
            return
        self.current_index = (self.current_index + 1) % len(self.tracks)
        self.play()

    def previous_track(self):
        if not self.tracks:
            return
        self.current_index = (self.current_index - 1) % len(self.tracks)
        self.play()

    def position_seconds(self):
        if not self.playing:
            return 0
        return max(0, pygame.mixer.music.get_pos() // 1000)
