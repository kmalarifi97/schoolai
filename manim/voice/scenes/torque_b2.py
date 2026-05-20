from manim import *
import numpy as np
from torque_helpers import make_bolt, make_wrench, force_arrow, rot_arrow

# "Then you slide a pipe over the handle to make it longer. Push gently.
#  It turns."
DUR = 7.19


class TorqueS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        P = np.array([-2.2, -0.4, 0])
        bolt = make_bolt(P, radius=0.42)
        short = make_wrench(P, length=2.0, angle=0.0)
        self.add(bolt, short)
        self.wait(0.5)
        # slide a pipe on -> longer handle
        long = make_wrench(P, length=4.4, angle=0.0)
        self.play(Transform(short, long), run_time=1.4)
        # gentle push at the far end
        tip = P + np.array([0.50 + 4.4, 0, 0])
        f = force_arrow(tip, [0, 0.85, 0], width=5)
        self.play(GrowArrow(f), run_time=0.8)
        # it turns
        ra = rot_arrow(P, radius=1.0, start_angle=-PI / 4, sweep=PI * 0.8)
        self.play(Rotate(VGroup(short, f), angle=PI * 0.42,
                          about_point=P),
                  Create(ra),
                  run_time=1.8, rate_func=rate_functions.ease_out_sine)
        self.wait(DUR - 5.0)
