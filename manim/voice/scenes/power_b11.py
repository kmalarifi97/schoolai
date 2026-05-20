from manim import *
import numpy as np
from power_helpers import big_label, small_label, WORK_COL, POWER_COL, TIME_COL

# "Energy is what you transfer. Power is how fast you transfer it."
DUR = 6.0


class PowerS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        e = big_label("Energy", [0, 1.7, 0], size=52, color=WORK_COL)
        eu = small_label("(joules)", [0, 0.85, 0], size=30, color=WORK_COL)
        self.play(FadeIn(e), FadeIn(eu), run_time=1.0)
        self.wait(0.5)

        line = Line([-3.0, 0.2, 0], [3.0, 0.2, 0], color="#EAE4D5",
                    stroke_width=2).set_opacity(0.4)
        p = big_label("Power", [0, -0.6, 0], size=52, color=POWER_COL)
        per = Text("(joules per ", font="sans", font_size=30,
                   color=POWER_COL)
        sec = Text("second", font="sans", font_size=30, color=TIME_COL)
        close = Text(")", font="sans", font_size=30, color=POWER_COL)
        unit = VGroup(per, sec, close).arrange(RIGHT, buff=0.06)
        unit.move_to([0, -1.5, 0])
        self.play(Create(line), run_time=0.5)
        self.play(FadeIn(p), FadeIn(unit), run_time=1.0)
        self.play(Indicate(sec, color=TIME_COL, scale_factor=1.3),
                  run_time=1.0)
        self.wait(max(0.3, DUR - 5.0))
