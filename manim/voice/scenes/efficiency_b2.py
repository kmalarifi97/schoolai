from manim import *
import numpy as np
from efficiency_helpers import (work_bar, bar_only, machine_block, stream,
                                label, WORK_COLOR, USEFUL_COLOR, FAINT_LABEL)

# "Build it in the real world and something is always missing."
DUR = 5.3


class EfficiencyS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        mac = machine_block([0, 0, 0], w=1.8, h=2.2)
        ib = work_bar(3.0, [-5.4, 0, 0], color=WORK_COLOR, max_length=3.0)
        st = stream([-1.9, 0, 0], [-1.05, 0, 0], width=6)
        self.add(mac, ib, st,
                 label("input work", [-3.9, 0.85, 0], size=24))

        # output comes out visibly shorter
        ob = bar_only(0.001, [1.1, 0, 0], color=USEFUL_COLOR)
        ghost = work_bar(3.0, [1.1, 0, 0], color=WORK_COLOR,
                         max_length=3.0)[0]
        ghost.set_stroke(FAINT_LABEL, width=1.4, opacity=0.6)
        self.add(ghost, ob)
        self.play(ob.animate.become(
            bar_only(1.7, [1.1, 0, 0], color=USEFUL_COLOR)), run_time=1.6)
        self.add(label("real output", [2.6, 0.85, 0], size=24,
                       color=USEFUL_COLOR))
        miss = label("something missing", [3.3, -0.95, 0], size=22,
                     color=FAINT_LABEL)
        self.play(FadeIn(miss), run_time=0.9)
        self.wait(DUR - 3.5)
