from manim import *
import numpy as np
from thermalbudget_helpers import energy_ledger, small_label

# "She wasn't short of heat. She was short of a budget — energy has
#  more than one bill to pay here."
DUR = 8.4


class ThermalbudgetS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # the chaos fades — a calm line
        t1 = small_label("not short of heat", [0, 2.0, 0],
                         color="#8C8576", size=24)
        self.play(FadeIn(t1), run_time=1.0)
        self.play(t1.animate.set_opacity(0.0), run_time=0.8)

        t2 = small_label("short of a budget", [0, 2.0, 0],
                         color="#EAE4D5", size=28)
        self.play(Write(t2), run_time=1.2)

        # a faint ledger with line-items waiting (empty bars)
        led = energy_ledger(
            [("raise temperature", 0.0, "#D98C5F"),
             ("hidden melt", 0.0, "#9BD6B0"),
             ("delivery rate", 0.0, "#B9BFC6")],
            [0, -0.7, 0], scale=0.95)
        led.set_opacity(0.5)
        self.play(FadeIn(led), run_time=1.4)
        self.wait(DUR - 4.4)
