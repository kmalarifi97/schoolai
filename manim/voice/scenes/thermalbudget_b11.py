from manim import *
import numpy as np
from thermalbudget_helpers import energy_ledger, small_label

# "Hidden melt cost, temperature cost, delivery rate. Miss one line and
#  the timing is always wrong."
DUR = 8.4


class ThermalbudgetS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        led = energy_ledger(
            [("hidden melt cost", 0.85, "#9BD6B0"),
             ("temperature cost", 0.55, "#D98C5F"),
             ("delivery rate", 0.5, "#B9BFC6")],
            [0, 0.5, 0], scale=1.0, title="thermal budget")
        self.play(FadeIn(led.rows[0]), run_time=0.9)
        self.play(FadeIn(led.rows[1]), run_time=0.9)
        self.play(FadeIn(led.rows[2]), run_time=0.9)
        self.play(FadeIn(led[1]), run_time=0.8)  # title

        warn = small_label("miss one line — timing always wrong",
                           [0, -2.4, 0], color="#D98C5F", size=24)
        self.play(Write(warn), run_time=1.4)
        self.wait(DUR - 5.8)
