from manim import *
import numpy as np
from heattransfer_helpers import (make_bowl, make_spoon, steam_wisps,
                                  heat_tint)

# "Hold a metal spoon in hot soup. Soon the handle, far from the soup,
#  is hot too."
DUR = 7.2


class HeattransferS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        bowl = make_bowl([0, -2.0, 0], scale=1.05)
        sp, handle = make_spoon([1.7, 2.3, 0], [-0.55, -1.85, 0],
                                scale=1.05)
        steam = steam_wisps([0, -1.55, 0], n=3, height=1.7)

        self.play(FadeIn(bowl), run_time=1.0)
        self.play(FadeIn(sp), run_time=1.0)
        self.add(steam)
        self.play(*[s.animate.set_stroke(opacity=0.45) for s in steam],
                  run_time=1.2)

        # heat creeps up the handle, segment by segment from soup end
        n = len(handle)
        anims = []
        for i, seg in enumerate(handle):
            anims.append(seg.animate.set_color(
                heat_tint(1.0 - i / (n - 1))))
        self.play(LaggedStart(*anims, lag_ratio=0.18, run_time=2.6))
        self.wait(DUR - 5.8)
