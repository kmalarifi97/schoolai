from manim import *
import numpy as np
from surfaceg_helpers import (
    make_person, make_world, radius_line, make_feather, make_hammer,
    make_equation_full, make_equation_reduced, label, qmark, divider,
    RED, CHALK, EARTH,
)


class SurfacegTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())
        # left world: earth with a person standing on top
        earth = make_world([-3.6, -1.0, 0], r=1.1, kind="earth")
        self.add(earth)
        person = make_person(scale=1.0)
        person.move_to([-3.6, earth.get_top()[1] + 0.5, 0])
        self.add(person)
        self.add(radius_line(earth, PI / 2, color=RED))
        self.add(label("r_E", [-2.4, -0.5, 0], size=24, color=RED))
        # feather + hammer
        self.add(make_feather([-1.2, 1.5, 0]))
        self.add(make_hammer([-0.4, 1.5, 0]))
        self.add(label("m_E", [-3.6, -2.3, 0], size=24, color=RED))
        # right: full equation top, reduced bottom
        eqf = make_equation_full([3.3, 1.4, 0], scale=1.2)
        self.add(eqf)
        eqr = make_equation_reduced([3.3, -0.6, 0], scale=1.2)
        self.add(eqr)
        # color-bind test: m_E and r_E red in both
        for eq in (eqf, eqr):
            p = eq.get_part_by_tex("m_E")
            if p: p.set_color(RED)
        # moon test
        moon = make_world([3.3, -2.4, 0], r=0.5, kind="moon")
        self.add(moon)
        self.wait(0.1)
