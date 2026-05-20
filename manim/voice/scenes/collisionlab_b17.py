from manim import *
import numpy as np
from collisionlab_helpers import energy_bar, cl_puck, small_label

# "After — she explains the gap. If the energy barely dropped, they
#  bounced. If it collapsed, they crushed together."
DUR = 9.6


class CollisionlabS1B17(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # left: elastic — energy bar nearly full, pucks apart
        eb1 = energy_bar(None, 0.90, [-4.4, 0.2, 0], color="#9BD6B0",
                         max_h=2.4, show_label=False)
        e1 = cl_puck([-3.4, -1.7, 0], r=0.24, color="#7FB8E8",
                     mass="")
        e2 = cl_puck([-2.4, -1.7, 0], r=0.24, color="#E8C46B",
                     mass="")
        ea1 = Arrow([-3.6, -1.7, 0], [-4.1, -1.7, 0], color="#9BD6B0",
                    stroke_width=3, buff=0,
                    max_tip_length_to_length_ratio=0.5)
        ea2 = Arrow([-2.2, -1.7, 0], [-1.7, -1.7, 0], color="#9BD6B0",
                    stroke_width=3, buff=0,
                    max_tip_length_to_length_ratio=0.5)
        el = small_label("bounced", [-3.4, -2.6, 0], color="#9BD6B0",
                         size=22)
        self.play(FadeIn(eb1), FadeIn(e1), FadeIn(e2),
                  GrowArrow(ea1), GrowArrow(ea2), FadeIn(el),
                  run_time=1.8)

        div = DashedLine([0, 2.4, 0], [0, -2.8, 0], color="#5A5446",
                         stroke_width=2).set_opacity(0.5)
        self.play(Create(div), run_time=0.8)

        # right: inelastic — energy collapsed, pucks fused
        eb2 = energy_bar(None, 0.22, [4.4, 0.2, 0], color="#D98C5F",
                         max_h=2.4, show_label=False)
        f1 = cl_puck([2.7, -1.7, 0], r=0.24, color="#7FB8E8", mass="")
        f2 = cl_puck([2.95, -1.7, 0], r=0.24, color="#E8C46B",
                     mass="")
        il = small_label("crushed together", [3.0, -2.6, 0],
                         color="#D98C5F", size=22)
        self.play(FadeIn(eb2), FadeIn(f1), FadeIn(f2), FadeIn(il),
                  run_time=1.8)
        self.wait(DUR - 4.4)
