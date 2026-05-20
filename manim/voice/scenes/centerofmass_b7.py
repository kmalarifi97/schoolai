from manim import *
import numpy as np
from centerofmass_helpers import (make_block, com_dot, ground_line,
                                  base_bracket, small_label)

# "Past that moment, it goes over. What flipped wasn't the push.
#  It was whether the center of mass stayed above the base."
DUR = 9.9

GY = -2.2


class CenterofmassS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        gl = ground_line(y=GY)
        W, H = 1.7, 2.6
        cx = -0.6
        blk = make_block(width=W, height=H, center=[cx, GY + H / 2, 0])
        bb = base_bracket(cx - W / 2, cx + W / 2, GY - 0.18)
        self.add(gl, bb, blk)

        pivot = np.array([cx + W / 2, GY, 0])
        com = com_dot([cx, GY + H / 2, 0], scale=0.85)

        def make_plumb():
            cp = com[0].get_center()
            return DashedLine(cp, np.array([cp[0], GY, 0]),
                              color="#E8B04A", stroke_width=2.4,
                              dash_length=0.13)
        plumb = always_redraw(make_plumb)

        def upd(m):
            m.move_to(blk.get_center())
        com.add_updater(upd)
        self.add(com, plumb)
        self.wait(0.5)

        grp = VGroup(blk, com)
        ang_tip = -np.arctan2(W / 2, H / 2)
        # to the tipping point
        self.play(Rotate(grp, angle=ang_tip, about_point=pivot),
                  run_time=2.2, rate_func=rate_functions.ease_out_sine)
        self.wait(0.7)
        # past it: the line crosses outside the base, it topples
        self.play(Rotate(grp, angle=-(PI / 2 - 0.05) - ang_tip,
                          about_point=pivot),
                  run_time=2.0, rate_func=rate_functions.ease_in_quad)
        com.clear_updaters()
        plumb.clear_updaters()
        self.wait(DUR - 7.4)
