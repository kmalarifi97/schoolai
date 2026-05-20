from manim import *
import numpy as np
from power_helpers import small_label, WORK_COL, TIME_COL, POWER_COL

# "Same work, less time — more power. Same work, more time — less
#  power. It's a rate."
DUR = 7.4


class PowerS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        WORK = 3.0  # constant

        # time slider track
        track = Line([-4.5, -2.4, 0], [-0.3, -2.4, 0], color=TIME_COL,
                     stroke_width=5)
        tval = ValueTracker(2.2)  # time value
        knob = Dot(radius=0.12, color=POWER_COL)
        knob.add_updater(lambda m: m.move_to(
            [-4.5 + (tval.get_value() - 0.6) / (3.4 - 0.6) * 4.2,
             -2.4, 0]))
        tlbl = small_label("time", [-2.4, -3.0, 0], size=26, color=TIME_COL)

        # power bar = WORK / time
        base_y = -2.4

        def make_bar():
            h = WORK / tval.get_value()
            return Rectangle(width=1.4, height=max(h, 0.01),
                             fill_color=POWER_COL, fill_opacity=0.92,
                             stroke_color=POWER_COL, stroke_width=2
                             ).move_to([3.0, base_y + max(h, 0.01) / 2, 0])

        pbar = always_redraw(make_bar)
        plbl = small_label("power", [3.0, -3.0, 0], size=26,
                           color=POWER_COL)

        self.play(Create(track), FadeIn(knob), FadeIn(tlbl),
                  FadeIn(pbar), FadeIn(plbl), run_time=1.2)
        self.wait(0.4)
        # time shrinks -> power shoots up
        self.play(tval.animate.set_value(0.7), run_time=1.6,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.5)
        # time grows -> power drops
        self.play(tval.animate.set_value(3.2), run_time=1.6,
                  rate_func=rate_functions.ease_in_out_sine)
        knob.clear_updaters()
        self.wait(max(0.3, DUR - 5.3))
