import time

# Elixir initial
red_elixir = 7.0
blue_elixir = 7.0

# Temps de départ
start_time = time.time()

# Limite max d'élixir
MAX_ELIXIR = 10

game = True

while game:

    # Temps écoulé depuis le début de la partie
    game_time = time.time() - start_time

    # skibidi ratio
    if game_time < 120:  # 0:00 -> 2:00 = x1
        regen_rate = 1 / 2.8  # 1 élixir toutes les 2.8 sec

    elif game_time < 180:  # 2:00 -> 3:00 = x2
        regen_rate = 2 / 2.8

    else:  # après 3:00 = x3
        regen_rate = 3 / 2.8

    # Temps entre chaque tick (60hz)
    delta = 0.1
    time.sleep(delta)

    # Régénération
    red_elixir += regen_rate * delta
    blue_elixir += regen_rate * delta

    red_elixir = min(red_elixir, MAX_ELIXIR)
    blue_elixir = min(blue_elixir, MAX_ELIXIR)
