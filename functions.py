import numpy as np

def get_turn_decision(junction, greens, threshold=100):
    directions = {"tr": False, "tl": False, "br": False, "bl": False}
    print("greens: ", greens, type(greens))
    for green in greens:
        dx, dy = green[0] - junction[0], green[1] - junction[1]

        if np.hypot(dx, dy) <= threshold:
            if dx > 0: directions["br" if dy > 0 else "tr"] = True
            elif dx < 0: directions["bl" if dy > 0 else "tl"] = True

    return directions