from manim import *
import numpy as np
from equivalence_helpers import (split_word_mass, make_block, make_hand,
                                 frictionless_plane, spring_scale,
                                 make_ball, sealed_box, side_panel,
                                 gravity_arrow, push_arrow, small_label)


class EquivalenceTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        whole, l, r = split_word_mass([-4.4, 2.6, 0], size=40)
        blk = make_block([-1.0, 2.4, 0], w=0.9, h=0.7)
        hand = make_hand([-2.1, 2.4, 0], facing=RIGHT)
        pa = push_arrow([-1.8, 2.4, 0], length=0.7)
        plane = frictionless_plane(y=1.4, x0=-6, x1=-0.5)
        spr, hp = spring_scale(top=np.array([2.4, 3.2, 0]), length=1.2)
        hb = make_block(hp + np.array([0, -0.5, 0]), w=0.7, h=0.6)
        ga = gravity_arrow(hp + np.array([0, -0.9, 0]), length=0.7)
        bb = make_ball([4.6, 2.4, 0], radius=0.34, big=True)
        lb = make_ball([5.5, 2.4, 0], radius=0.34, big=False)
        np_ = side_panel([-3.4, -1.4, 0], w=4.0, h=3.0, title="Newton")
        ep = side_panel([3.4, -1.4, 0], w=4.0, h=3.0, title="Einstein")
        box1, _ = sealed_box([-3.4, -1.4, 0], size=2.0)
        box2, _ = sealed_box([3.4, -1.4, 0], size=2.0, with_flame=True)
        self.add(whole, l, r, blk, hand, pa, plane, spr, hb, ga,
                 bb, lb, np_, ep, box1, box2)
        self.add(small_label("test", [0, 3.4, 0], size=22))
        self.wait(0.4)
