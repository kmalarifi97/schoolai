from manim import *
import numpy as np
from thermolaws_helpers import engine_box, efficiency_dial, small_label

# "It's why no engine is perfect. Some energy must always be paid out
#  as disordered waste heat. You can't even break even."
DUR = 9.6


class ThermolawsS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        eng = engine_box([0, -0.4, 0], scale=1.0, show_waste=True)
        self.play(FadeIn(eng), run_time=1.4)
        self.wait(0.5)
        # the dial, pinned below 100%
        dial = efficiency_dial([0, 2.6, 0], pct=8, scale=1.0)
        self.play(FadeIn(dial[0]), FadeIn(dial[1]), run_time=0.8)
        self.play(FadeIn(dial[3]), FadeIn(dial[5]), run_time=0.4)
        # needle climbs but jams below 100%
        for p in (35, 58, 64):
            d2 = efficiency_dial([0, 2.6, 0], pct=p, scale=1.0)
            self.play(Transform(dial, d2), run_time=0.8)
        # unavoidable waste-heat stream pulses
        wst = eng[8]
        self.play(Indicate(wst, color="#8A5340", scale_factor=1.15),
                  run_time=1.0)
        be = small_label("can't even break even", [0, -3.3, 0], size=24,
                         color="#C0473A")
        self.play(FadeIn(be), run_time=0.8)
        self.wait(DUR - 7.3)
