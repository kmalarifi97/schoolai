from manim import *
import numpy as np
from elasticpe_helpers import (make_spring, wall_block, spring_mass,
                               make_bar, set_bar, small_label)

# "Within its limit, though, it's a perfect bank. Put energy in by
#  bending; take it back when it springs."
DUR = 8.8


class ElasticpeS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        wx = -4.6
        wall = wall_block([wx, 0.4, 0], h=1.6)
        rest_x = -2.0
        spring = make_spring([wx + 0.15, 0.4, 0], [rest_x, 0.4, 0],
                             coils=10, amp=0.28)
        mass = spring_mass([rest_x + 0.3, 0.4, 0], r=0.30)
        bar = make_bar([4.0, 0.4, 0], max_h=2.6, frac=0.0,
                       color="#E8C46A", label="energy bank")
        self.add(wall, spring, mass, bar["group"])
        self.wait(0.4)

        stretched_x = 1.4

        def s_at(x):
            return make_spring([wx + 0.15, 0.4, 0], [x, 0.4, 0],
                               coils=10, amp=0.28)

        def m_at(x):
            return spring_mass([x + 0.3, 0.4, 0], r=0.30)

        for _ in range(2):
            # load: stretch, bar fills
            self.play(Transform(spring, s_at(stretched_x)),
                      Transform(mass, m_at(stretched_x)),
                      Transform(bar["fill"], set_bar(bar, 0.9)),
                      run_time=1.1,
                      rate_func=rate_functions.ease_in_out_sine)
            # release: springs back, bar empties into motion
            self.play(Transform(spring, s_at(rest_x)),
                      Transform(mass, m_at(rest_x)),
                      Transform(bar["fill"], set_bar(bar, 0.0)),
                      run_time=0.9,
                      rate_func=rate_functions.ease_out_quad)
        self.wait(DUR - 4.4)
