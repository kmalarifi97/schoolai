from manim import *
import numpy as np
from thermalbudget_helpers import (efc_layout, play_button,
                                   small_label)

# "Here is the real job. Not pressing play. Predicting — before she
#  does."
DUR = 6.5


class ThermalbudgetS1B14(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        efc = efc_layout([-2.0, 0.4, 0], scale=0.8, heat=0.5,
                         melt=0.0, chunks=True)
        # chunks paused at the source — clustered low near the heater
        for c in efc.chunks:
            c.move_to([efc.heater.get_center()[0]
                       + np.random.uniform(-0.3, 0.3),
                       efc.heater.get_top()[1] + 0.15, 0])
        self.add(efc)

        pb = play_button([2.6, -0.6, 0], r=0.5)
        self.play(FadeIn(pb), run_time=0.8)

        # a finger hovers, deliberately not pressing
        finger = Arrow([4.0, -0.6, 0], [3.2, -0.6, 0],
                       color="#EAE4D5", stroke_width=5, buff=0,
                       max_tip_length_to_length_ratio=0.3)
        self.play(GrowArrow(finger), run_time=1.0)
        self.play(finger.animate.shift(RIGHT * 0.25), run_time=1.0,
                  rate_func=rate_functions.there_and_back)

        t = small_label("predict first", [2.6, 1.8, 0],
                        color="#9BD6B0", size=24)
        self.play(FadeIn(t), run_time=0.7)
        self.wait(DUR - 4.3)
