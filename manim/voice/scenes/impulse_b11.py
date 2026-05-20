from manim import *
import numpy as np
from impulse_helpers import (icon_airbag, icon_knees, icon_boxer,
                             small_label, F_COLOR)

# "Airbags, knees bending on landing, a boxer rolling with a punch—all
#  the same trick. Buy time, cut the force. Watch: the airbag stretches
#  the stop from a tenth of a second to half a second—force drops
#  fivefold."
DUR = 16.5


class ImpulseS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        ab = icon_airbag(1.0).move_to([-4.2, 1.7, 0])
        kn = icon_knees(1.0).move_to([0.0, 1.7, 0])
        bx = icon_boxer(1.0).move_to([4.2, 1.7, 0])
        ab_l = small_label("airbag", [-4.2, 0.5, 0], color="#8C98A6",
                           size=24)
        kn_l = small_label("knees bending", [0.0, 0.5, 0],
                           color="#8C98A6", size=24)
        bx_l = small_label("rolling with it", [4.2, 0.5, 0],
                           color="#8C98A6", size=24)
        self.play(FadeIn(ab, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(kn, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(bx, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(ab_l), FadeIn(kn_l), FadeIn(bx_l), run_time=0.7)

        trick = small_label("buy time, cut the force", [0, -0.4, 0],
                            color="#EAE4D5", size=30)
        self.play(Write(trick), run_time=1.1)
        self.wait(0.5)

        # airbag numeric annotation: 0.1s -> 0.5s, force 5x -> 1x
        self.play(trick.animate.set_opacity(0.25),
                  Indicate(ab, color="#E8C25A", scale_factor=1.12),
                  run_time=1.0)

        t_before = small_label("time:  0.1 s", [-3.0, -1.3, 0],
                               color="#8C98A6", size=26)
        t_after = small_label("time:  0.5 s", [-3.0, -1.3, 0],
                              color="#EAE4D5", size=26)
        self.play(FadeIn(t_before), run_time=0.7)

        f_big = Arrow([2.2, -0.9, 0], [2.2, -2.3, 0], buff=0,
                      color=F_COLOR, stroke_width=9)
        f_big_l = small_label("force ×5", [3.3, -1.6, 0],
                              color=F_COLOR, size=26)
        self.play(GrowArrow(f_big), FadeIn(f_big_l), run_time=0.9)
        self.wait(0.6)

        # stretch the time, shrink the force fivefold
        f_small = Arrow([2.2, -1.45, 0], [2.2, -1.73, 0], buff=0,
                        color=F_COLOR, stroke_width=5)
        f_small_l = small_label("force ×1", [3.3, -1.6, 0],
                                color="#7FB890", size=26)
        self.play(Transform(t_before, t_after),
                  Transform(f_big, f_small),
                  Transform(f_big_l, f_small_l),
                  run_time=1.6, rate_func=rate_functions.ease_in_out_sine)

        drop = small_label("stretch the stop  →  force drops fivefold",
                           [0, -3.0, 0], color="#7FB890", size=24)
        self.play(FadeIn(drop), run_time=0.9)
        self.wait(DUR - 12.3)
