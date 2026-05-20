from manim import *
import numpy as np
from skatepark_helpers import make_ramp, make_faris, arc_path

# "The ramp keeps lying to him. Same setup, different result. He can't
#  see the rule underneath."
DUR = 8.1


class SkateparkS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        r = make_ramp(launch_h=2.4)
        self.add(r["group"])
        faris = make_faris([-2.9, r["ground_y"] + 0.55, 0], scale=0.85)
        self.play(FadeIn(faris), run_time=1.0)

        # the two contradicting arcs hang faintly above him
        short_end = np.array([r["gap_x1"] - 0.3,
                              r["ground_y"] - 0.05, 0])
        over_end = np.array([6.2, r["ground_y"] - 0.05, 0])
        a1 = arc_path(r["lip"], short_end, peak=1.2, color="#C98A6B",
                      width=3).set_opacity(0.45)
        a2 = arc_path(r["lip"], over_end, peak=1.7, color="#9BD6B0",
                      width=3).set_opacity(0.45)
        self.play(FadeIn(a1), FadeIn(a2), run_time=1.4)
        # a held, quiet beat — he just sits with it
        self.wait(DUR - 2.4)
