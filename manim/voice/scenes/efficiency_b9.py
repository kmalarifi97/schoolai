from manim import *
import numpy as np
from efficiency_helpers import (bar_only, machine_block, stream, label,
                                WORK_COLOR, HEAT_COLOR, FAINT_LABEL)

# "And in a compound machine the losses stack. Each stage skims a little
#  off the top."
DUR = 6.7


class EfficiencyS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        stages_x = [-3.2, 0.0, 3.2]
        lens = [3.0, 2.3, 1.7, 1.2]      # bar entering / between / out
        ys = 0.0

        # input bar
        b = bar_only(0.001, [-6.0, ys, 0], color=WORK_COLOR, height=0.55)
        self.add(b)
        self.play(b.animate.become(
            bar_only(lens[0], [-6.0, ys, 0], color=WORK_COLOR,
                     height=0.55)), run_time=0.8)

        prev_right = -6.0 + lens[0]
        for k, sx in enumerate(stages_x):
            mac = machine_block([sx, ys, 0], w=1.0, h=1.4)
            self.play(FadeIn(mac), run_time=0.5)
            # loss skimmed at this stage
            loss = stream([sx, ys + 0.5, 0], [sx, ys + 1.3, 0],
                          color=HEAT_COLOR, width=3)
            # shorter bar emerges after the stage
            start_x = sx + 0.6
            nb = bar_only(0.001, [start_x, ys, 0], color=WORK_COLOR,
                          height=0.55)
            self.add(nb)
            self.play(GrowArrow(loss),
                      nb.animate.become(
                          bar_only(lens[k + 1], [start_x, ys, 0],
                                   color=WORK_COLOR, height=0.55)),
                      run_time=0.9)

        self.add(label("losses stack", [0, -1.7, 0], size=24,
                       color=FAINT_LABEL))
        self.add(label("each stage skims off the top", [0, 2.2, 0],
                       size=22, color=HEAT_COLOR))
        self.wait(DUR - 4.7)
