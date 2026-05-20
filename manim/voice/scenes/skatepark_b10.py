from manim import *
import numpy as np
from skatepark_helpers import make_ramp, plywood_stack, arc_path

# "But he was never short of wood. He was short of a model."
DUR = 5.5


class SkateparkS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        r = make_ramp(launch_h=2.4)
        self.add(r["group"])
        short_end = np.array([r["gap_x1"] - 0.3,
                              r["ground_y"] - 0.05, 0])
        over_end = np.array([6.2, r["ground_y"] - 0.05, 0])
        a1 = arc_path(r["lip"], short_end, peak=1.2, color="#C98A6B",
                      width=3).set_opacity(0.55)
        a2 = arc_path(r["lip"], over_end, peak=1.7, color="#9BD6B0",
                      width=3).set_opacity(0.55)
        self.add(a1, a2)
        stack = plywood_stack([5.0, r["ground_y"] + 0.4, 0], n=4, w=1.5)
        self.add(stack)
        self.wait(0.6)
        # the plywood fades; the arcs remain, waiting to be explained
        self.play(FadeOut(stack), run_time=1.6)
        self.wait(DUR - 2.2)
