from manim import *
import numpy as np
from power_helpers import big_label, small_label, WORK_COL, TIME_COL, POWER_COL

# "Computing power as work divided by time — and as force times speed
#  — for a real climb or engine — that's yours."
DUR = 9.5


class PowerS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        pw = Text("power", font="sans", font_size=52, color=POWER_COL)
        eq = Text("=", font="sans", font_size=52, color="#EAE4D5")
        wk = Text("work", font="sans", font_size=46, color=WORK_COL)
        bar = Line([0, 0, 0], [1.7, 0, 0], color="#EAE4D5", stroke_width=4)
        tm = Text("time", font="sans", font_size=46, color=TIME_COL)
        frac = VGroup(wk, bar, tm).arrange(DOWN, buff=0.16)
        row = VGroup(pw, eq, frac).arrange(RIGHT, buff=0.35)
        row.move_to([0, 0.6, 0])
        bar.set_width(max(wk.width, tm.width) + 0.2)

        self.play(FadeIn(pw), run_time=0.8)
        self.play(FadeIn(eq), run_time=0.4)
        self.play(FadeIn(wk), Create(bar), FadeIn(tm), run_time=1.2)
        self.wait(0.6)

        alt = small_label("= force x speed", [0, -1.7, 0], size=34,
                          color=POWER_COL)
        self.play(FadeIn(alt), run_time=0.9)
        self.wait(0.5)
        yours = small_label("the numbers — yours", [0, -2.8, 0], size=26
                            ).set_opacity(0.6)
        self.play(FadeIn(yours), run_time=0.9)
        self.wait(max(0.4, DUR - 6.7))
