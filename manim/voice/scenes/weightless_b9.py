from manim import *
import numpy as np
from weightless_helpers import earth_limb, curved_fall_arc, small_label

# "Throw it harder. It lands farther. Harder still — farther still."
DUR = 5.7

CX, CY, R = 0.0, -8.0, 7.4


class WeightlessS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([CX, CY, 0])
        limb = earth_limb(C, R)
        self.add(limb)

        # launch from the top of the limb, three progressively longer arcs
        th0 = np.pi / 2 + 0.18  # just left of top
        spans = [0.30, 0.55, 0.85]
        drops = [0.55, 0.95, 1.4]
        cols = ["#E8C97F", "#E8C97F", "#E8C97F"]
        ops = [0.45, 0.7, 1.0]
        for span, drop, col, op in zip(spans, drops, cols, ops):
            arc = curved_fall_arc(C, R, th0, th0 - span, drop, color=col)
            arc.set_stroke(opacity=op)
            self.play(Create(arc), run_time=1.1,
                      rate_func=rate_functions.ease_out_sine)
        self.add(small_label("farther", [3.1, 0.2, 0], size=24))
        self.wait(DUR - 3.5)
