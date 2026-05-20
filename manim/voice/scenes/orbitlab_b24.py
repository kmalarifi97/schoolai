from manim import *
import numpy as np
from orbitlab_helpers import (callback_rocks, callback_field,
                              callback_thrown, make_planet,
                              closed_circle_path)

# "This orbit was all three at once. That is the concept. Now you know
#  which videos to go back to."
# visual ends with: [Hold 3s in silence] -- honored as a held final
# still frame, 3s added to this scene's run time. No literal text.
BASE_DUR = 8.3
HOLD = 3.0
DUR = BASE_DUR + HOLD


class OrbitlabS1B24(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # the three callbacks present, spread out, faint
        rocks = callback_rocks([-4.2, 1.7, 0], scale=0.9, opacity=0.8)
        field = callback_field([0.0, 2.0, 0], scale=0.85, opacity=0.8)
        thrown = callback_thrown([4.2, 1.8, 0], scale=0.85,
                                 opacity=0.8)
        self.play(FadeIn(rocks), FadeIn(field), FadeIn(thrown),
                  run_time=1.4)
        self.wait(0.8)

        # they converge toward the center and dissolve. FadeOut (not
        # set_opacity) so the closed thrown-arc never fills as a disc.
        center = np.array([0, 0.1, 0])
        self.play(
            FadeOut(rocks, target_position=center, scale=0.3),
            FadeOut(field, target_position=center, scale=0.3),
            FadeOut(thrown, target_position=center, scale=0.3),
            run_time=2.0, rate_func=rate_functions.ease_in_out_sine)

        # ... into the single planet + closed-orbit trace
        c = np.array([0, 0.1, 0])
        planet = make_planet(c, r=0.75)
        circ = closed_circle_path(c, r=1.9, color="#9BD6B0", width=4)
        self.play(FadeIn(planet, scale=1.05),
                  Create(circ), run_time=1.8)

        # the concept, complete. Stillness. [Hold 3s in silence]
        self.wait(BASE_DUR - 6.0)
        self.wait(HOLD)            # the deliberate 3s silent hold
