from manim import *
import numpy as np
from torque_helpers import (make_bolt, make_wrench, force_arrow, rot_arrow,
                            small_label)

# "Less force. More effect. Something other than force is doing the work
#  here."
DUR = 6.9


class TorqueS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # LEFT: big force, short handle, no turn
        PL = np.array([-3.6, 1.4, 0])
        boltL = make_bolt(PL, radius=0.34)
        wrL = make_wrench(PL, length=1.5, angle=0.0)
        fL = force_arrow(PL + np.array([0.40 + 1.5, 0, 0]),
                         [0, 1.4, 0], width=9)
        xmark = Text("✕", font="sans", font_size=40, color="#C46A5A"
                     ).move_to(PL + np.array([0.6, -1.0, 0]))
        self.add(boltL, wrL, fL)
        # RIGHT: small force, long handle, turns
        PR = np.array([-3.6, -1.7, 0])
        boltR = make_bolt(PR, radius=0.34)
        wrR = make_wrench(PR, length=4.2, angle=0.0)
        fR = force_arrow(PR + np.array([0.40 + 4.2, 0, 0]),
                         [0, 0.75, 0], width=5)
        self.add(boltR, wrR, fR)
        self.wait(0.6)
        self.play(FadeIn(xmark), run_time=0.6)
        ra = rot_arrow(PR, radius=0.9, start_angle=-PI / 4, sweep=PI * 0.7)
        self.play(Rotate(VGroup(wrR, fR), angle=PI * 0.34,
                          about_point=PR),
                  Create(ra),
                  run_time=1.8, rate_func=rate_functions.ease_out_sine)
        self.wait(DUR - 3.8)
