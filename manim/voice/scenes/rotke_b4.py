from manim import *
import numpy as np
from rotke_helpers import (make_flywheel, axis_pin, make_hand,
                           spark_burst)

# "Try to stop it with your hand. It bites back. It clearly carries
#  something."
DUR = 6.9


class RotkeS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([-0.4, 0, 0])
        R = 1.8
        fw = make_flywheel(C, radius=R)
        self.add(fw, axis_pin(C, scale=1.1))
        # fast spin
        speed = [2.4]
        fw.add_updater(lambda m, dt: m.rotate(-speed[0] * dt,
                                               about_point=C))
        self.wait(1.0)

        contact = C + np.array([R + 0.05, 0, 0])
        hand = make_hand(0.85)
        # hand reaches in from the right toward the rim
        hand.move_to(contact + np.array([1.8, 0, 0]))
        self.play(hand.animate.move_to(contact + np.array([0.62, 0, 0])),
                  run_time=1.0)
        sparks = spark_burst(contact, n=10, r_out=0.55)
        self.play(Create(sparks), run_time=0.4)
        # it bites back: hand shoved out a touch, sparks flare, spin
        # reluctantly drops
        self.play(hand.animate.shift(RIGHT * 0.28 + UP * 0.10),
                  sparks.animate.scale(1.25).set_opacity(0.7),
                  run_time=0.5)
        speed[0] = 0.7
        self.play(FadeOut(sparks), run_time=0.6)
        self.wait(DUR - 4.5)
        fw.clear_updaters()
