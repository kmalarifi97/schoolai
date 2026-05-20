from manim import *
import numpy as np
from centerofmass_helpers import (wide_shape, tall_shape, com_dot,
                                  ground_line, base_bracket, small_label)

# "This is why a low, wide thing is hard to tip. A race car. A pyramid."
DUR = 5.8

GY = -2.0


class CenterofmassS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        gl = ground_line(y=GY)

        # low + wide on the left
        ws = wide_shape(center=[-3.0, GY + 0.55, 0])
        wcom = com_dot([-3.0, GY + 0.45, 0], scale=0.72)
        wbb = base_bracket(-4.7, -1.3, GY - 0.16)
        wtag = small_label("hard to tip", [-3.0, GY - 0.7, 0], size=24,
                           color="#7FB8E8")

        # tall + narrow on the right
        ts = tall_shape(center=[3.2, GY + 1.5, 0])
        tcom = com_dot([3.2, GY + 1.5, 0], scale=0.72)
        tbb = base_bracket(3.2 - 0.42, 3.2 + 0.42, GY - 0.16)

        self.add(gl)
        self.play(FadeIn(VGroup(ws, wcom, wbb)),
                  FadeIn(VGroup(ts, tcom, tbb)), run_time=1.0)
        self.wait(0.4)

        # tilt the wide one a lot — com stays over the base
        pivW = np.array([-1.3, GY, 0])
        gW = VGroup(ws, wcom)
        self.play(Rotate(gW, angle=-0.30, about_point=pivW),
                  run_time=1.2, rate_func=rate_functions.there_and_back)
        wcom.move_to(ws.get_center() + DOWN * 0.10)
        self.play(FadeIn(wtag, shift=UP * 0.15), run_time=0.8)
        self.wait(DUR - 3.4)
