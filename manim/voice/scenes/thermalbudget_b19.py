from manim import *
import numpy as np
from thermalbudget_helpers import (run_counter, predict_vs_result,
                                   small_label)

# "Her first prediction is wrong. That is not the problem. That is the
#  point. Each miss exposes a line she forgot."
DUR = 9.5


class ThermalbudgetS1B19(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # run 1 off
        pvr1 = predict_vs_result([-3.4, 0.3, 0], pred=0.35, res=0.85)
        rc1 = run_counter([-3.4, -2.0, 0], used=1, total=3)
        self.play(FadeIn(pvr1), FadeIn(rc1), run_time=1.2)
        w = small_label("wrong", [-3.4, 2.0, 0], color="#D98C5F",
                        size=22)
        self.play(FadeIn(w), run_time=0.6)

        # run 2 closer
        pvr2 = predict_vs_result([0, 0.3, 0], pred=0.55, res=0.72)
        rc2 = run_counter([0, -2.0, 0], used=2, total=3)
        self.play(FadeIn(pvr2), FadeIn(rc2), run_time=1.2)

        # run 3 right on the buzzer
        pvr3 = predict_vs_result([3.4, 0.3, 0], pred=0.7, res=0.72)
        rc3 = run_counter([3.4, -2.0, 0], used=3, total=3)
        self.play(FadeIn(pvr3), FadeIn(rc3), run_time=1.2)
        ok = small_label("on the buzzer", [3.4, 2.0, 0],
                         color="#9BD6B0", size=22)
        self.play(FadeIn(ok), run_time=0.7)
        self.wait(DUR - 5.1)
