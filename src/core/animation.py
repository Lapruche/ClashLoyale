class Animation:
    def __init__(self, frames, frame_duration, loop=True):
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop

        self.current_frame = 0
        self.timer = 0

        self.finished = False
        self.playing = True

    def update(self, dt):
        if not self.playing or self.finished:
            return

        self.timer += dt

        while self.timer >= self.frame_duration:
            self.timer -= self.frame_duration
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
                    break

    @property
    def current_sprite(self):
        return self.frames[self.current_frame]

    def stop(self):
        self.playing = False

    def play(self):
        self.playing = True

    def reset(self):
        self.current_frame = 0
        self.timer = 0
        self.finished = False
