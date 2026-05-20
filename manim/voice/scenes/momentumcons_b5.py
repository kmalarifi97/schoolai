from manim import *
import numpy as np
from momentumcons_helpers import (momentum_bar, zero_line, label,
                                  PLUS_COL, MINUS_COL)

# "The bag's forward momentum and your backward momentum are equal and
#  opposite. They cancel."
DUR = 7.9


class MomentumconsS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        origin = (0, 1.2, 0)
        zl = zero_line(origin, height=3.0)
        bar_p = momentum_bar(1.8, +1, origin=origin, unit=1.4,
                             color=PLUS_COL)
        bar_m = momentum_bar(1.8, -1, origin=origin, unit=1.4,
                             color=MINUS_COL)
        self.add(zl, bar_p, bar_m)
        self.add(label("bag, forward", (1.9, 2.0, 0), color=PLUS_COL,
                       size=22))
        self.add(label("you, backward", (-1.9, 2.0, 0), color=MINUS_COL,
                       size=22))
        self.wait(0.9)

        # lay them against each other below — equal and opposite
        cmp_o = np.array([0, -1.6, 0])
        cp = momentum_bar(1.8, +1, origin=cmp_o, unit=1.4, color=PLUS_COL)
        cm = momentum_bar(1.8, -1, origin=cmp_o, unit=1.4, color=MINUS_COL)
        self.play(
            bar_p.copy().animate.move_to(cp.get_center()),
            bar_m.copy().animate.move_to(cm.get_center()),
            run_time=1.6,
        )
        self.add(cp, cm)
        eq = label("equal and opposite", (0, -2.6, 0), color="#8C98A6",
                   size=24)
        self.play(FadeIn(eq), run_time=0.8)
        # they cancel — fade together to nothing
        self.play(cp.animate.set_opacity(0.0),
                  cm.animate.set_opacity(0.0), run_time=1.3)
        cancel = label("they cancel", (0, -1.6, 0), color="#EAE4D5",
                       size=28)
        self.play(FadeIn(cancel), run_time=0.7)
        self.wait(DUR - 5.3)
