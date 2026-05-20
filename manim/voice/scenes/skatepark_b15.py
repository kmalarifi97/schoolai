from manim import *
import numpy as np
from skatepark_helpers import phet_track, bar_chart_panel, small_label

# "Energy Skate Park. He builds his ramp's shape into the track. Turns
#  the energy bars on."
DUR = 7.8


class SkateparkS1B15(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        title = small_label("Energy Skate Park", [0, 3.2, 0],
                            color="#8C8576", size=24)
        self.play(FadeIn(title), run_time=0.8)
        track = phet_track([-2.4, -0.4, 0], launch_h=2.0, scale=1.0)
        self.play(Create(track[0]), run_time=2.0)
        self.wait(0.4)
        panel = bar_chart_panel([3.4, -0.2, 0], pe=0.85, ke=0.05,
                                th=0.0, scale=0.85)
        # bars switch on
        self.play(FadeIn(panel, shift=UP * 0.2), run_time=1.4)
        self.wait(DUR - 4.6)
