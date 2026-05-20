from manim import *
import numpy as np
from balancerig_helpers import make_mobile

# "She hangs the shapes. The bar swings hard to the right and stays
#  there."
DUR = 6.6


class BalancerigS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        m = make_mobile([0, 0.3, 0], half_w=3.0,
                        shapes=[(-1.6, 0.6, "#9BD6B0"),
                                (1.4, 0.9, "#C98A6B"),
                                (2.6, 0.8, "#E8C46B")],
                        ceil_y=3.4)
        self.add(m["ceiling"], m["string"])
        self.play(FadeIn(m["rig"], shift=UP * 0.15), run_time=1.4)
        self.wait(0.6)
        pv = m["string"].get_end()
        # swings hard right, then settles there (a small recoil)
        self.play(Rotate(m["rig"], angle=-0.52, about_point=pv),
                  run_time=1.2, rate_func=rate_functions.ease_in_sine)
        self.play(Rotate(m["rig"], angle=0.06, about_point=pv),
                  run_time=0.5,
                  rate_func=rate_functions.ease_out_sine)
        self.play(Rotate(m["rig"], angle=-0.06, about_point=pv),
                  run_time=0.5)
        self.wait(DUR - 4.2)
