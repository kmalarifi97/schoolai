from manim import *
import numpy as np
from skatepark_helpers import make_ramp, ideal_arc

# "One goal. Clear the gap. Land clean on the far side."
DUR = 5.2


class SkateparkS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        r = make_ramp(launch_h=2.0)
        self.add(r["group"])
        self.wait(0.5)
        arc = ideal_arc(r["lip"], r["land_top"], peak=1.6)
        self.play(Create(arc), run_time=2.0,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(DUR - 2.5)
