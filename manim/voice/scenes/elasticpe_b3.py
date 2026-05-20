from manim import *
import numpy as np
from elasticpe_helpers import make_bow, make_bar, flying_arrow

# "Let go. The arrow leaves at terrific speed. The work was never lost.
#  It was loaded into the bend."
DUR = 8.5


class ElasticpeS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        bow = make_bow([1.2, 0, 0], draw=0.85, scale=1.2)
        self.add(bow["group"])
        bar = make_bar([4.6, 0.1, 0], max_h=2.4, frac=0.85,
                       color="#E8C46A", label="stored")
        self.add(bar["group"])
        self.wait(0.6)

        # release: limbs + string snap to relaxed; arrow flies off left
        relaxed = make_bow([1.2, 0, 0], draw=0.0, scale=1.2)
        fly = flying_arrow(bow["nock_pt"], length=2.1)
        empty = make_bar([4.6, 0.1, 0], max_h=2.4, frac=0.0,
                         color="#E8C46A")
        self.remove(bow["arrow"])
        self.add(fly)
        self.play(
            Transform(bow["limbs"], relaxed["limbs"]),
            Transform(bow["string"], relaxed["string"]),
            Transform(bow["nock"], relaxed["nock"]),
            run_time=0.5, rate_func=rate_functions.ease_out_quad)
        self.play(
            fly.animate.shift(LEFT * 7.0),
            Transform(bar["fill"], empty["fill"]),
            run_time=1.3, rate_func=rate_functions.ease_out_quad)
        self.wait(DUR - 4.7)
