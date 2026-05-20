from manim import *
import numpy as np
from skatepark_helpers import make_ramp, phet_track, bar_chart_panel

# "So before he touches the real ramp again — he tests it somewhere he
#  can see the energy."
DUR = 7.8


class SkateparkS1B14(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        r = make_ramp(launch_h=2.4)
        self.add(r["group"])
        self.wait(0.6)
        # the plywood ramp resolves into the Skate Park layout
        track = phet_track([-2.4, -0.4, 0], launch_h=2.0, scale=1.0)
        panel = bar_chart_panel([3.4, -0.2, 0], pe=0.85, ke=0.05,
                                th=0.0, scale=0.85)
        self.play(FadeOut(r["group"]), run_time=1.2)
        self.play(Create(track[0]), run_time=1.6)
        self.play(FadeIn(panel), run_time=1.2)
        self.wait(DUR - 4.6)
