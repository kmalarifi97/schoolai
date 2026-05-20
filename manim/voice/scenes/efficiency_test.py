from manim import *
import numpy as np
from efficiency_helpers import (work_bar, bar_only, machine_block, winch,
                                make_load, heat_shimmer, stream,
                                percent_dial, split_bar, label,
                                WORK_COLOR, USEFUL_COLOR, HEAT_COLOR)


class EfficiencyTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        ib = work_bar(2.4, [-6.4, 2.6, 0], color=WORK_COLOR, max_length=3.0)
        ob = work_bar(1.5, [-2.6, 2.6, 0], color=USEFUL_COLOR, max_length=3.0)
        mac = machine_block([4.0, 2.4, 0], w=1.4, h=1.6)

        w = winch([-4.6, -1.0, 0], scale=0.9)
        load = make_load([-4.6, -2.9, 0])
        heat = heat_shimmer([-3.9, -0.9, 0], n=4, spread=0.5, rise=0.6)

        dial = percent_dial([1.0, -1.4, 0], 78, scale=0.8)

        sb = split_bar(3.0, [3.5, -2.8, 0], 0.62, height=0.5)
        st = stream([-1.2, 2.6, 0], [0.2, 2.6, 0])

        self.add(ib, ob, mac, w["group"], load, heat, dial["group"],
                 sb, st,
                 label("input", [-5.2, 3.3, 0], size=20),
                 label("output", [-1.4, 3.3, 0], size=20),
                 label("winch", [-4.6, 0.3, 0], size=20))
        self.wait(0.4)
