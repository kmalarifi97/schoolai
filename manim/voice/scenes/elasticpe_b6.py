from manim import *
import numpy as np
from elasticpe_helpers import (make_spring, wall_block, spring_mass,
                               resist_arrow, small_label)

# "Stretch a little, store a little. Stretch more, and it fights back
#  harder the farther you go."
DUR = 8.2


class ElasticpeS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        wx = -5.0
        wall = wall_block([wx, 0.6, 0], h=1.6)
        rest_end = -2.6
        spring = make_spring([wx + 0.15, 0.6, 0], [rest_end, 0.6, 0],
                             coils=10, amp=0.28)
        mass = spring_mass([rest_end + 0.3, 0.6, 0], r=0.28)
        self.add(wall, spring, mass)
        self.wait(0.5)

        steps = [(-1.0, 0.55), (0.6, 1.05), (2.2, 1.6)]
        prev_arrow = None
        for end_x, force_len in steps:
            new_spring = make_spring([wx + 0.15, 0.6, 0], [end_x, 0.6, 0],
                                     coils=10, amp=0.28)
            new_mass = spring_mass([end_x + 0.3, 0.6, 0], r=0.28)
            arr = resist_arrow([end_x + 0.62, 0.6, 0], force_len)
            anims = [Transform(spring, new_spring),
                     Transform(mass, new_mass)]
            if prev_arrow is None:
                anims.append(GrowArrow(arr))
            else:
                anims.append(Transform(prev_arrow, arr))
            self.play(*anims, run_time=1.0,
                      rate_func=rate_functions.ease_in_out_sine)
            if prev_arrow is None:
                prev_arrow = arr
            self.wait(0.25)
        self.wait(DUR - 4.75)
