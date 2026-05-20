from manim import *
import numpy as np
from torque_helpers import (make_door_topdown, force_arrow, rot_arrow,
                            small_label)

# "A door proves it daily. Push at the handle, it swings. Push next to
#  the hinge, it fights you."
DUR = 8.2


class TorqueS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # LEFT: push at the handle -> swings wide
        HL = np.array([-3.6, 1.6, 0])
        doorL = make_door_topdown(HL, length=3.2, angle=0.0)
        self.add(doorL)
        self.wait(0.5)
        endL = HL + np.array([3.2 - 0.22, 0, 0])
        fL = force_arrow(endL + np.array([0, 0.9, 0]), [0, -0.8, 0],
                         width=7)
        self.play(GrowArrow(fL), run_time=0.7)
        raL = rot_arrow(HL, radius=1.6, start_angle=-PI / 14,
                        sweep=-PI * 0.42, color="#7FB8E8")
        self.play(Rotate(VGroup(doorL, fL), angle=-PI * 0.42,
                          about_point=HL),
                  Create(raL),
                  run_time=1.6, rate_func=rate_functions.ease_out_sine)
        self.add(small_label("push at the handle",
                             HL + np.array([1.4, -2.2, 0]), size=22))

        # RIGHT: push next to the hinge -> barely moves
        HR = np.array([1.4, 1.6, 0])
        doorR = make_door_topdown(HR, length=3.2, angle=0.0)
        self.add(doorR)
        nearR = HR + np.array([0.7, 0, 0])
        fR = force_arrow(nearR + np.array([0, 0.9, 0]), [0, -0.8, 0],
                         width=7)
        self.play(GrowArrow(fR), run_time=0.7)
        self.play(Rotate(VGroup(doorR, fR), angle=-PI * 0.05,
                          about_point=HR),
                  run_time=1.2, rate_func=rate_functions.ease_out_sine)
        self.add(small_label("push near the hinge",
                             HR + np.array([1.4, -2.2, 0]), size=22))
        self.wait(DUR - 5.7)
