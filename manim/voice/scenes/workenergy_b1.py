from manim import *
import numpy as np
from workenergy_helpers import make_figure, make_wall, sweat_drop

# "Push hard against a wall for an hour. You're exhausted. The wall hasn't moved."
DUR = 7.1


class WorkenergyS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        wall = make_wall([1.4, 0, 0], height=4.6)
        fig = make_figure([-0.6, -0.6, 0], scale=1.05, straining=True,
                          facing=1)
        self.play(FadeIn(wall, run_time=1.0))
        self.play(FadeIn(fig, run_time=1.0))
        self.wait(0.8)
        # strain shimmer + a sweat drop falling
        drop = sweat_drop([-0.2, 0.6, 0])
        self.play(FadeIn(drop, run_time=0.4))
        self.play(drop.animate.shift(DOWN * 1.5).set_opacity(0),
                  run_time=1.2)
        self.wait(0.4)
        # the wall does not move — hold on stillness
        self.wait(DUR - 5.4)
