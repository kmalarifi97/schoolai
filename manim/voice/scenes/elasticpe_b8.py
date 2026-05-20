from manim import *
import numpy as np
from elasticpe_helpers import make_bow, make_bar, small_label

# "That's why a slightly longer draw on the bow sends the arrow much
#  farther than you'd guess."
DUR = 8.1


class ElasticpeS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # top: shorter draw -> modest stored bar
        bowA = make_bow([-2.4, 1.5, 0], draw=0.55, scale=0.85)
        self.add(bowA["group"])
        barA = make_bar([3.4, 1.5, 0], max_h=1.8, w=0.55, frac=0.0,
                        color="#E8C46A")
        self.add(barA["group"])
        la = small_label("draw x", [-2.4, 0.1, 0], size=22)
        self.add(la)
        fullA = make_bar([3.4, 1.5, 0], max_h=1.8, w=0.55, frac=0.30,
                         color="#E8C46A")
        self.play(Transform(barA["fill"], fullA["fill"]), run_time=1.0)
        self.wait(0.4)

        # bottom: slightly longer draw -> dramatically larger bar
        bowB = make_bow([-2.4, -1.6, 0], draw=0.85, scale=0.85)
        self.add(bowB["group"])
        barB = make_bar([3.4, -1.6, 0], max_h=1.8, w=0.55, frac=0.0,
                        color="#E8C46A")
        self.add(barB["group"])
        lb = small_label("draw x + a little", [-2.2, -3.0, 0], size=22)
        self.add(lb)
        fullB = make_bar([3.4, -1.6, 0], max_h=1.8, w=0.55, frac=0.92,
                         color="#E8C46A")
        self.play(Transform(barB["fill"], fullB["fill"]),
                  run_time=1.2, rate_func=rate_functions.ease_out_quad)
        self.wait(DUR - 4.6)
