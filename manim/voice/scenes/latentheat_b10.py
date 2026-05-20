from manim import *
import numpy as np
from latentheat_helpers import (make_skin, droplet, energy_arrows,
                                small_label)

# "It's why sweat cools you: evaporating water carries off enormous
#  hidden energy as it leaves your skin."
DUR = 9.3


class LatentheatS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        skin = make_skin([0, -1.6, 0], w=6.0, h=1.0)
        self.play(FadeIn(skin), run_time=1.0)

        drops = VGroup(*[droplet([x, -1.35, 0], r=0.16)
                         for x in (-2.2, -0.8, 0.6, 2.0)])
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.1) for d in drops],
                              lag_ratio=0.15, run_time=1.2))
        self.wait(0.4)

        # each droplet evaporates upward carrying an energy arrow away
        for d in drops:
            c = d.get_center()
            up = Arrow(c, c + np.array([0, 1.3, 0]), color="#F2A24E",
                       stroke_width=4, buff=0,
                       max_tip_length_to_length_ratio=0.3)
            self.play(d.animate.shift(UP * 1.2).set_opacity(0.0),
                      GrowArrow(up), run_time=0.7)
            self.play(up.animate.shift(UP * 0.5).set_opacity(0.0),
                      run_time=0.4)

        lbl = small_label("hidden energy leaves — skin cools",
                          [0, 2.0, 0], color="#8C98A6", size=24)
        self.play(FadeIn(lbl), run_time=0.8)
        self.wait(DUR - 6.9)
