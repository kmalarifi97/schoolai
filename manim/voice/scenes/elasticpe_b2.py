from manim import *
import numpy as np
from elasticpe_helpers import make_bow, make_bar, small_label

# "You did work to draw it. The bow isn't moving — so where is that
#  work now?"
DUR = 6.8


class ElasticpeS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        bow = make_bow([-1.6, 0, 0], draw=0.85, scale=1.2)
        self.add(bow["group"])
        self.wait(0.4)
        bar = make_bar([3.6, 0.1, 0], max_h=2.4, frac=0.0,
                       color="#E8C46A", label="work done")
        self.add(bar["group"])
        full = make_bar([3.6, 0.1, 0], max_h=2.4, frac=0.85,
                        color="#E8C46A")
        self.play(Transform(bar["fill"], full["fill"]), run_time=1.4)
        self.wait(0.4)
        q = Text("?", font="sans", font_size=66, color="#EAE4D5"
                 ).move_to([0.9, 0.0, 0])
        self.play(FadeIn(q, scale=0.6), run_time=1.0)
        self.wait(DUR - 3.6)
