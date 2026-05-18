ONCE = 0


class Animation:
    def __init__(self):
        # Animation en cours (doit contenir .frames et .playmode)
        self.anim = None

        # Index de la frame actuelle
        self.frame_num = 0

        # Image actuelle et suivante
        self.current = None
        self.next = None

        # Liste des frames jouées pendant cette update
        self.played = []

        # Progression entre current et next (utile pour interpolation)
        self.transition = 0.0

        # État de lecture
        self.playing = True

        # Temps total écoulé depuis le début de l’animation
        self.playtime = 0.0

        # Durée totale de la frame actuelle
        self.frame_time = 0.0

        # Temps restant avant de passer à la frame suivante
        self.timeleft = 0.0

        # Vitesse de lecture (1.0 = normal, 2.0 = 2x plus rapide, etc.)
        self.playspeed = 1.0

    def use_anim(self, anim):
        # Assigne une nouvelle animation
        self.anim = anim
        self.reset()

    def reset(self):
        # Remet l’animation à zéro

        self.frame_num = 0

        # Initialise la première frame
        self.current = self.anim.frames[0][0]

        # Temps de la première frame
        self.timeleft = self.anim.frames[0][1]
        self.frame_time = self.timeleft

        # Calcule la frame suivante (boucle avec modulo)
        next_frame = (self.frame_num + 1) % len(self.anim.frames)
        self.next = self.anim.frames[next_frame][0]

        # Réinitialise le temps global et la transition
        self.playtime = 0.0
        self.transition = 0.0

    def play(self, playspeed=1.0):
        # Lance l’animation avec une vitesse donnée
        self.playspeed = playspeed
        self.reset()
        self.unpause()

    def pause(self):
        # Met en pause l’animation
        self.playing = False

    def unpause(self):
        # Reprend l’animation
        self.playing = True

    def update(self, dt):
        """
        Met à jour l’animation

        dt = delta time (temps écoulé depuis la dernière frame, en secondes)
        """

        dt *= self.playspeed

        self.played = []

        if not self.playing or not self.anim:
            return

        self.playtime += dt

        self.timeleft -= dt

        if self.frame_time > 0:
            self.transition = self.timeleft / self.frame_time

        while self.timeleft <= 0.0:

            self.frame_num = (self.frame_num + 1) % len(self.anim.frames)

            if self.anim.playmode == ONCE and self.frame_num == 0:
                self.pause()
                return

            next_frame = (self.frame_num + 1) % len(self.anim.frames)

            frame, time = self.anim.frames[self.frame_num]

            self.frame_time = time
            self.timeleft += time

            self.current = frame
            self.next = self.anim.frames[next_frame][0]

            self.played.append(frame)

            if time > 0:
                self.transition = self.timeleft / time

            if self.frame_num == 0:
                self.playtime = self.timeleft
