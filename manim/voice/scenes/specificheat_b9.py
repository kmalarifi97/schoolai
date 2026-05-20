from manim import *
import numpy as np
from specificheat_helpers import engine_block, water_bottle, clock, label
from specificheat_helpers import WATER_COL

# "It's why water cools an engine, why a hot-water bottle stays warm for
#  hours."
DUR = 6.8


class SpecificheatS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        en = engine_block([-3.4, 0.2, 0], scale=1.0)
        le = label("engine — cooled", [-3.4, -1.6, 0], size=22)
        # coolant loop around the engine
        loop = RoundedRectangle(width=3.0, height=2.4, corner_radius=0.4,
                                color=WATER_COL, stroke_width=4,
                                fill_opacity=0).move_to([-3.4, 0.2, 0])
        wb = water_bottle([3.2, 0.1, 0], scale=0.95)
        ck = clock([4.9, 1.3, 0], scale=0.6)
        lb = label("warm for hours", [3.2, -1.9, 0], size=22)
        self.play(FadeIn(en), run_time=0.9)
        self.play(Create(loop), FadeIn(le), run_time=1.2)
        dot = Dot(color=WATER_COL, radius=0.09).move_to(loop.get_start())
        self.play(MoveAlongPath(dot, loop), run_time=1.6,
                  rate_func=linear)
        self.play(FadeOut(dot), FadeIn(wb), FadeIn(ck), FadeIn(lb),
                  run_time=1.0)
        self.wait(DUR - 4.7)
