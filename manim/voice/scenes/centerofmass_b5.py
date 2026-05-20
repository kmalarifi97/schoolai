from manim import *
import numpy as np
from centerofmass_helpers import (make_block, com_dot, ground_line,
                                  base_bracket, small_label)

# "Now stand a block on the table. Tilt it a little. It rocks back down."
DUR = 5.8

GY = -2.2


class CenterofmassS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        gl = ground_line(y=GY)
        W, H = 1.7, 2.6
        cx = 0.0
        blk = make_block(width=W, height=H, center=[cx, GY + H / 2, 0])
        bb = base_bracket(cx - W / 2, cx + W / 2, GY - 0.18)
        self.add(gl, bb, blk)

        pivot = np.array([cx + W / 2, GY, 0])  # bottom-right corner
        com = com_dot([cx, GY + H / 2, 0], scale=0.85)

        def upd(m):
            m.move_to(blk.get_center())
        com.add_updater(upd)
        self.add(com)
        self.wait(0.6)

        grp = VGroup(blk, com)
        # small tilt about the corner, then rock back
        self.play(Rotate(grp, angle=-0.22, about_point=pivot),
                  run_time=1.4, rate_func=rate_functions.ease_out_sine)
        self.wait(0.4)
        self.play(Rotate(grp, angle=0.22, about_point=pivot),
                  run_time=1.4, rate_func=rate_functions.ease_in_sine)
        com.clear_updaters()
        self.wait(DUR - 4.8)
