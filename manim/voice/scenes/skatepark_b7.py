from manim import *
import numpy as np
from skatepark_helpers import make_ramp, arc_path, qmark, small_label

# "Same height as before. But now he flies further — and overshoots
#  again. The same ramp gave him two different answers."
DUR = 9.9


class SkateparkS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        r = make_ramp(launch_h=2.4)          # SAME height as b5
        self.add(r["group"])
        self.wait(0.5)

        # yesterday's run (rough): falls just short
        short_end = np.array([r["gap_x1"] - 0.3,
                              r["ground_y"] - 0.05, 0])
        rough_arc = arc_path(r["lip"], short_end, peak=1.2,
                             color="#C98A6B", width=4)
        self.play(Create(rough_arc), run_time=1.6)
        lbl_r = small_label("rough", short_end + np.array([0.1, 0.5, 0]),
                            color="#C98A6B", size=22)
        self.play(FadeIn(lbl_r), run_time=0.6)
        self.wait(0.6)

        # today's run (waxed): SAME start, flies much further, overshoots
        over_end = np.array([6.2, r["ground_y"] - 0.05, 0])
        wax_arc = arc_path(r["lip"], over_end, peak=1.7,
                           color="#9BD6B0", width=4)
        self.play(Create(wax_arc), run_time=1.8)
        lbl_w = small_label("waxed", np.array([4.4, 1.4, 0]),
                            color="#9BD6B0", size=22)
        self.play(FadeIn(lbl_w), run_time=0.6)

        # a faint question mark between the two
        q = qmark([0.0, 1.7, 0], size=56)
        self.play(FadeIn(q), run_time=0.8)
        self.wait(DUR - 7.3)
