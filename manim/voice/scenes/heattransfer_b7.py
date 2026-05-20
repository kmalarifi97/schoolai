from manim import *
import numpy as np
from heattransfer_helpers import convection_loop, small_label

# "Heat carried by the bulk motion of a fluid. That's convection."
DUR = 6.0


class HeattransferS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        loop = convection_loop([0, 0.4, 0], w=3.4, h=2.4)
        self.add(loop)
        self.wait(0.5)

        lbl = small_label("convection — by flow", [0, -2.0, 0],
                          color="#E0552B", size=30)
        self.play(Write(lbl), run_time=1.4)

        # faint icons: wind + ocean current driven by the same engine
        wind = small_label("~  wind", [-2.6, -3.0, 0],
                           color="#7E8A96", size=22).set_opacity(0.6)
        ocean = small_label("~  ocean currents", [2.4, -3.0, 0],
                            color="#7E8A96", size=22).set_opacity(0.6)
        self.play(FadeIn(wind), FadeIn(ocean), run_time=1.0)
        self.wait(DUR - 3.9)
