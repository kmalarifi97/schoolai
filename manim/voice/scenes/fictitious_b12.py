from manim import *
import numpy as np
from fictitious_helpers import (rotating_disk, split_divider, frame_label,
                                big_label, PATH_COL, LABEL_COL)

# "These forces vanish the moment you step to the still ground. When do
#  you need them, and how big are they? That's the thinking to carry
#  off."
DUR = 10.7


class FictitiousS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(split_divider(0.0))

        LC = np.array([-3.5, 0.2, 0])
        RC = np.array([3.5, 0.2, 0])
        R = 1.9

        disk = rotating_disk(LC, radius=R, n_spokes=8)
        still = Circle(radius=R, fill_color="#1B2530", fill_opacity=1,
                       stroke_color=LABEL_COL, stroke_width=2.5
                       ).move_to(RC)
        self.play(FadeIn(disk), FadeIn(still), run_time=1.2)

        lcap = frame_label("rotating frame", LC + np.array([0, 2.6, 0]),
                           size=24)
        rcap = frame_label("still ground", RC + np.array([0, 2.6, 0]),
                           size=24)
        lsub = frame_label("forces appear", LC + np.array([0, -2.6, 0]),
                           color=PATH_COL, size=22)
        rsub = frame_label("forces vanish", RC + np.array([0, -2.6, 0]),
                           color=LABEL_COL, size=22)
        self.play(FadeIn(lcap), FadeIn(rcap), run_time=0.9)

        self.play(Rotate(disk, angle=PI * 0.6, about_point=LC),
                  FadeIn(lsub), FadeIn(rsub),
                  run_time=2.2, rate_func=rate_functions.linear)

        q = big_label("when?   how big?", [0, -3.3, 0], size=34)
        self.play(FadeIn(q), run_time=1.0)
        # the open question holds
        self.wait(DUR - 5.3)
