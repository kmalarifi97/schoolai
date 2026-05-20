from manim import *
import numpy as np
from latentheat_helpers import (make_skin, steam_curl, energy_bar,
                                small_label)

# "And it runs in reverse. Steam releases that hidden energy when it
#  condenses—which is why steam delivers far more heat to skin than
#  boiling water at the same temperature."
DUR = 15.3


class LatentheatS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # left: steam hitting skin
        skin_l = make_skin([-3.4, -1.4, 0], w=3.4, h=0.7)
        st = VGroup(steam_curl([-3.9, -0.4, 0], scale=0.8),
                    steam_curl([-3.0, -0.3, 0], scale=0.7))
        self.play(FadeIn(skin_l), Create(st), run_time=1.4)
        lbl_s = small_label("steam, 100°", [-3.4, 1.6, 0],
                            color="#C8D6E0", size=24)
        self.play(FadeIn(lbl_s), run_time=0.7)

        # right: boiling water touching skin
        skin_r = make_skin([3.4, -1.4, 0], w=3.4, h=0.7)
        wdrop = VGroup(*[Circle(radius=0.12, color="#5E86A8",
                                fill_opacity=0.6, stroke_width=1.5
                                ).move_to([3.4 + 0.5 * i, -0.6, 0])
                         for i in (-1, 0, 1)])
        self.play(FadeIn(skin_r), FadeIn(wdrop), run_time=1.2)
        lbl_w = small_label("boiling water, 100°", [3.4, 1.6, 0],
                            color="#5E86A8", size=24)
        self.play(FadeIn(lbl_w), run_time=0.7)

        # energy bars compared: steam dumps a big one
        big = energy_bar([-1.1, 0.55, 0], 0.92, "from steam",
                         max_h=2.4, w=0.7, color="#F2A24E")
        small = energy_bar([1.1, 0.55, 0], 0.30, "from water",
                           max_h=2.4, w=0.7, color="#F2A24E")
        cap = small_label("energy delivered to skin", [0, -2.6, 0],
                          color="#8C98A6", size=24)
        self.play(GrowFromEdge(big[1], DOWN),
                  FadeIn(big[0]), FadeIn(big[2]), run_time=1.3)
        self.play(GrowFromEdge(small[1], DOWN),
                  FadeIn(small[0]), FadeIn(small[2]), run_time=1.3)
        self.play(FadeIn(cap), run_time=0.8)
        self.wait(DUR - 9.4)
