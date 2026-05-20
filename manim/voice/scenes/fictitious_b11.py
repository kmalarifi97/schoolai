from manim import *
import numpy as np
from fictitious_helpers import make_globe, curved_flow, frame_label

# "We live on one. The Earth is the spinning platform. It steers winds
#  and ocean currents into great curves."
DUR = 8.6


class FictitiousS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, 0, 0])
        globe, _ = make_globe(C, radius=2.4)
        self.play(FadeIn(globe, scale=0.85), run_time=1.4)

        # broad atmospheric / ocean flow arcs curving across the globe
        f1 = curved_flow(C, 1.7, span=PI * 0.55, start_ang=2.4,
                         clockwise=True)
        f2 = curved_flow(C, 1.1, span=PI * 0.55, start_ang=-0.5,
                         clockwise=True)
        f3 = curved_flow(C, 2.05, span=PI * 0.5, start_ang=1.0,
                         clockwise=False)
        self.play(Create(f1), run_time=1.0)
        self.play(Create(f2), Create(f3), run_time=1.2)

        flows = VGroup(f1, f2, f3)
        self.play(Rotate(globe, angle=-PI * 0.35, about_point=C),
                  Rotate(flows, angle=-PI * 0.35, about_point=C),
                  run_time=2.4, rate_func=rate_functions.linear)
        self.wait(DUR - 6.0)
