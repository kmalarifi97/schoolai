from manim import *
import numpy as np
from tempvsthermal_helpers import (make_match, make_bathtub, make_room,
                                   small_label)

# "The match is hotter, but it can't warm the room. The cooler tub can.
#  Hotter isn't the same as more heat."
DUR = 9.0


class TempvsthermalS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # match + its tiny room
        match = make_match([-5.0, 0.2, 0], scale=0.85)
        room_m = make_room([-3.0, -0.2, 0], scale=0.66)
        self.add(match, room_m)
        # the match's energy is a tiny glow that barely reaches the room
        glow = Dot([-4.4, 0.2, 0], radius=0.10, color="#FF7A3C")
        self.play(FadeIn(match), FadeIn(room_m), run_time=0.8)
        self.play(glow.animate.scale(1.4).set_opacity(0.25),
                  run_time=1.2, rate_func=rate_functions.there_and_back)
        self.add(small_label("hotter — but barely any heat", [-4.0, -2.4, 0],
                             size=20, color="#FF7A3C"))

        # tub + its room, the room fills with warmth
        tub = make_bathtub([2.0, -0.3, 0], scale=0.66)
        room_t = make_room([5.0, -0.1, 0], scale=0.78)
        self.play(FadeIn(tub), FadeIn(room_t), run_time=0.9)
        warm = Rectangle(width=2.0, height=1.55, fill_color="#E58A4C",
                         fill_opacity=0.0, stroke_width=0
                         ).move_to([5.0, -0.25, 0])
        self.add(warm)
        self.play(warm.animate.set_fill(opacity=0.5), run_time=1.6)
        self.add(small_label("cooler — but warms the room", [4.6, -2.4, 0],
                             size=20, color="#8FB8D8"))
        self.wait(DUR - 5.4)
