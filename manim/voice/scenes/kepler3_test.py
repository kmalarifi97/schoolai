from manim import *
import numpy as np
from kepler3_helpers import (
    make_sun, make_planet, orbit_ring, planet_on_ring, radius_line,
    make_clock, clock_wedge, clock_hand, label, qmark, divider,
    make_equation, PLANET_A, PLANET_B, RED, CHALK,
)


class Kepler3Test(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # left world
        Lc = np.array([-3.6, 0.4, 0])
        self.add(make_sun(Lc, scale=0.7))
        self.add(orbit_ring(Lc, r=1.4))
        pa = planet_on_ring(Lc, 1.4, PI / 2, r=0.18, color=PLANET_A)
        self.add(pa)
        self.add(radius_line(Lc, PI / 2, 1.4, color=RED))
        clk = make_clock([-3.6, -2.4, 0], r=0.45)
        self.add(clk)
        self.add(clock_wedge(clk, 0.35, color=RED))
        self.add(clock_hand(clk, 0.35))
        self.add(label("r", [-3.0, 1.5, 0], size=26, color=RED))
        self.add(label("T", [-3.0, -2.4, 0], size=26, color=CHALK))
        self.add(divider())
        # right equation
        eq = make_equation([3.2, 0.3, 0], scale=1.2)
        self.add(eq)
        # try to recolor r terms red and subscripts
        # introspect: print tex strings count via labels
        for i, sub in enumerate(eq.submobjects):
            try:
                t = sub.get_tex_string()
            except Exception:
                t = "?"
        self.wait(0.1)
