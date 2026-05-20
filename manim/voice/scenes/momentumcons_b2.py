from manim import *
import numpy as np
from momentumcons_helpers import frozen_lake, make_figure, make_bag

# "You slide backward. You didn't push the ground. The bag did nothing
#  to the world but leave your hands."
DUR = 8.6


class MomentumconsS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        lake = frozen_lake((0, 0, 0))
        fig = make_figure((-0.7, 0, 0), scale=1.0)
        bag = make_bag((0.4, 0, 0), scale=0.95)
        self.add(lake, fig, bag)
        self.wait(0.8)
        # the bag flies forward (right), the figure glides backward (left)
        self.play(
            bag.animate.move_to([5.4, 0, 0]),
            fig.animate.move_to([-3.0, 0, 0]),
            run_time=2.4, rate_func=rate_functions.ease_out_quad,
        )
        self.wait(DUR - 4.2)
