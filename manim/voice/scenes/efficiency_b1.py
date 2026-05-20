from manim import *
import numpy as np
from efficiency_helpers import (work_bar, bar_only, machine_block, stream,
                                label, WORK_COLOR)

# "A perfect machine: every bit of work you put in comes out the other side."
DUR = 6.7


class EfficiencyS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        mac = machine_block([0, 0, 0], w=1.8, h=2.2)
        self.play(FadeIn(mac), run_time=1.0)

        in_pos = [-5.4, 0, 0]
        ib = work_bar(3.0, in_pos, color=WORK_COLOR, max_length=3.0)
        self.play(GrowFromEdge(ib[1], LEFT), FadeIn(ib[0]), run_time=1.2)
        self.add(label("input work", [-3.9, 0.85, 0], size=24))

        st = stream([-1.9, 0, 0], [-1.05, 0, 0], width=6)
        self.play(GrowArrow(st), run_time=0.6)

        # equal output comes out the other side
        ob = bar_only(0.001, [1.1, 0, 0], color=WORK_COLOR)
        self.add(ob)
        self.play(ob.animate.become(
            bar_only(3.0, [1.1, 0, 0], color=WORK_COLOR)), run_time=1.4)
        self.add(label("output work", [2.6, 0.85, 0], size=24))
        self.wait(DUR - 4.2)
