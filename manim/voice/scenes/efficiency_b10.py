from manim import *
import numpy as np
from efficiency_helpers import (bar_only, label, WORK_COLOR, USEFUL_COLOR,
                                HEAT_COLOR, FAINT_LABEL)

# "This is why ideal mechanical advantage and the real one disagree. The
#  gap is exactly what friction ate."
DUR = 8.6


class EfficiencyS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # ideal MA bar (tall)
        ideal = bar_only(0.001, [-3.8, 1.1, 0], color=WORK_COLOR,
                         height=0.62)
        self.add(ideal)
        self.play(ideal.animate.become(
            bar_only(4.0, [-3.8, 1.1, 0], color=WORK_COLOR, height=0.62)),
            run_time=1.0)
        self.add(label("ideal MA", [-4.6, 1.1, 0], size=24,
                       color=WORK_COLOR))

        # real MA bar (shorter)
        real = bar_only(0.001, [-3.8, -1.1, 0], color=USEFUL_COLOR,
                        height=0.62)
        self.add(real)
        self.play(real.animate.become(
            bar_only(2.5, [-3.8, -1.1, 0], color=USEFUL_COLOR,
                     height=0.62)), run_time=1.0)
        self.add(label("real MA", [-4.6, -1.1, 0], size=24,
                       color=USEFUL_COLOR))

        # the gap = what friction ate
        gap = Rectangle(width=1.5, height=0.62, fill_color=HEAT_COLOR,
                        fill_opacity=0.5, stroke_color=HEAT_COLOR,
                        stroke_width=1.5)
        gap.move_to([-3.8 + 2.5 + 0.75, -1.1, 0])
        self.play(FadeIn(gap), run_time=1.0)
        brace = label("the gap = what friction ate", [1.0, -2.4, 0],
                      size=24, color=HEAT_COLOR)
        self.play(Write(brace), run_time=1.4)
        self.wait(DUR - 5.4)
