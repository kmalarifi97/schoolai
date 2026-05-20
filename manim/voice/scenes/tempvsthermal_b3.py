from manim import *
import numpy as np
from tempvsthermal_helpers import (make_match, make_bathtub, make_room,
                                   q_mark, small_label)

# "Now: which one could you safely touch — and which one could heat a
#  whole room?"
DUR = 7.1


class TempvsthermalS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        match = make_match([-4.6, 0.2, 0], scale=0.9)
        tub = make_bathtub([2.4, -0.4, 0], scale=0.72)
        room = make_room([5.4, -0.3, 0], scale=0.62)
        self.add(match, tub, room)
        self.wait(0.5)

        # a hand (simple) approaching the match
        hand = RoundedRectangle(width=0.55, height=0.35, corner_radius=0.12,
                                fill_color="#D8A87A", fill_opacity=1,
                                stroke_width=0).move_to([-3.0, 0.0, 0])
        self.play(hand.animate.move_to([-3.7, 0.0, 0]), run_time=1.2)
        q1 = q_mark([-4.6, 2.0, 0], size=54)
        self.play(FadeIn(q1, scale=0.6), run_time=0.8)

        q2 = q_mark([3.9, 1.6, 0], size=54)
        self.play(FadeIn(q2, scale=0.6), run_time=0.8)
        self.add(small_label("safe to touch?", [-4.6, -2.3, 0],
                             size=22, color="#8FB8D8"),
                 small_label("heat the room?", [3.9, -2.3, 0],
                             size=22, color="#8FB8D8"))
        self.wait(DUR - 4.6)
