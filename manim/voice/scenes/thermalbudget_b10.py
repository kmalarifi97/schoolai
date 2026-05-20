from manim import *
import numpy as np
from thermalbudget_helpers import (energy_ledger, small_label,
                                   METAL, ICE)

# "And the rate the bill arrives depends on what carries the heat —
#  fast through metal, slow otherwise."
DUR = 8.7


class ThermalbudgetS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        led = energy_ledger(
            [("delivery rate", 0.0, "#B9BFC6")],
            [0, 2.2, 0], scale=1.0)
        self.play(FadeIn(led), run_time=0.9)

        # a metal path: heat dots travel fast
        m_lbl = small_label("metal — fast", [-3.6, 1.1, 0],
                            color="#B9BFC6", size=22)
        m_line = Line([-5.4, 0.4, 0], [-1.6, 0.4, 0], color=METAL,
                      stroke_width=6)
        self.play(FadeIn(m_lbl), Create(m_line), run_time=1.0)
        d1 = Dot([-5.4, 0.4, 0], radius=0.10, color="#D98C5F")
        self.add(d1)
        self.play(d1.animate.move_to([-1.6, 0.4, 0]), run_time=0.9,
                  rate_func=rate_functions.linear)

        # a poor path: heat dot crawls
        p_lbl = small_label("otherwise — slow", [3.0, 1.1, 0],
                            color="#8C8576", size=22)
        p_line = Line([1.4, 0.4, 0], [5.2, 0.4, 0], color=ICE,
                      stroke_width=4).set_opacity(0.6)
        self.play(FadeIn(p_lbl), Create(p_line), run_time=1.0)
        d2 = Dot([1.4, 0.4, 0], radius=0.10, color="#D98C5F")
        self.add(d2)
        led_full = energy_ledger(
            [("delivery rate", 0.55, "#B9BFC6")],
            [0, 2.2, 0], scale=1.0)
        self.play(d2.animate.move_to([5.2, 0.4, 0]),
                  Transform(led, led_full), run_time=2.2,
                  rate_func=rate_functions.linear)
        self.wait(DUR - 6.0)
