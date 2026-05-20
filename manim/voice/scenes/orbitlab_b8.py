from manim import *
import numpy as np
from orbitlab_helpers import make_planet, make_moon, gravity_arrow

# "The planet always pulls the moon straight toward its center. That
#  pull never rests."
DUR = 7.5


class OrbitlabS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        c = np.array([0, 0, 0])
        planet = make_planet(c, r=0.85)
        self.add(planet)

        # the moon at several places; the inward arrow redrawn each time
        positions = [
            c + np.array([2.4, 0.0, 0]),
            c + np.array([1.4, 1.9, 0]),
            c + np.array([-2.0, 1.4, 0]),
            c + np.array([-2.3, -1.0, 0]),
            c + np.array([0.6, -2.2, 0]),
        ]
        moon = make_moon(positions[0], r=0.16)
        arr = gravity_arrow(positions[0], c, length=0.95,
                            color="#D98C5F")
        self.play(FadeIn(moon), GrowArrow(arr), run_time=1.0)
        for p in positions[1:]:
            new_arr = gravity_arrow(p, c, length=0.95, color="#D98C5F")
            self.play(moon.animate.move_to(p),
                      Transform(arr, new_arr),
                      run_time=1.1,
                      rate_func=rate_functions.ease_in_out_sine)
        self.wait(DUR - 5.4)
