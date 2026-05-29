from manim import *
import numpy as np
from weighearth_helpers import (
    make_earth, radius_line, make_sun, make_planet, make_scale,
    make_cavendish, make_stone, make_equation_g, make_equation_mE,
    label, qmark, divider, RED, CHALK,
)


class WeighearthTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())
        # earth top-left
        earth = make_earth([-4.5, 1.4, 0], r=0.8)
        self.add(earth, radius_line(earth, color=RED))
        # scale bottom-left
        self.add(make_scale([-4.5, -1.5, 0], scale=0.8))
        # cavendish middle-left
        self.add(make_cavendish([-1.8, -1.4, 0], scale=0.8))
        # stone + sun + planet near top
        self.add(make_stone([-2.2, 1.6, 0]))
        self.add(make_sun([-1.2, 1.6, 0], scale=0.5))
        self.add(make_planet([-0.4, 1.6, 0]))
        # equations right
        eqg = make_equation_g([3.3, 1.4, 0], scale=1.2)
        eqg.get_part_by_tex("m_E").set_color(RED)
        self.add(eqg)
        eqm = make_equation_mE([3.3, -0.8, 0], scale=1.2)
        eqm.get_part_by_tex("m_E").set_color(RED)
        self.add(eqm)
        self.add(qmark([-4.5, -2.7, 0], size=50))
        self.wait(0.1)
