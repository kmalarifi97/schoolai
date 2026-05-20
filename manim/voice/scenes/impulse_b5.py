from manim import *
import numpy as np
from impulse_helpers import momentum_bar, small_label, P_COLOR, F_COLOR

# "To change momentum you need a force. But force alone isn't the whole
#  story."
DUR = 6.9


class ImpulseS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        block = Square(side_length=0.9, fill_color=P_COLOR,
                       fill_opacity=0.85, stroke_color="#4A6E8C",
                       stroke_width=2).move_to([0.6, 1.4, 0])
        self.add(block)

        push = Arrow(block.get_left() + LEFT * 1.5,
                     block.get_left() + LEFT * 0.05, buff=0,
                     color=F_COLOR, stroke_width=6)
        f_lbl = small_label("force", push.get_center()
                            + np.array([0, 0.4, 0]), color=F_COLOR,
                            size=26)
        self.play(GrowArrow(push), FadeIn(f_lbl), run_time=1.0)

        bar = momentum_bar(1.0, length=3.6, height=0.5).move_to(
            [0, -1.4, 0])
        self.play(GrowFromEdge(bar, LEFT), run_time=1.0)

        # force shrinks the momentum bar
        new_fill = bar.bar_fill.copy().stretch_to_fit_width(
            bar.bar_fill.width * 0.45)
        new_fill.align_to(bar.bar_frame, LEFT)
        self.play(Transform(bar.bar_fill, new_fill), run_time=1.6,
                  rate_func=rate_functions.ease_in_out_sine)

        note = small_label("force alone isn't the whole story",
                           [0, -2.7, 0], color="#8C98A6", size=24)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(DUR - 5.4)
