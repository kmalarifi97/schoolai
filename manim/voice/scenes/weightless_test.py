from manim import *
import numpy as np
from weightless_helpers import (
    make_earth, make_astronaut, make_station, make_scale, make_person,
    make_elevator, make_cable, big_label, small_label, question_mark,
    earth_limb, ballistic_arc, curved_fall_arc, orbit_circle, point_on_circle)


class WeightlessTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        astro = make_astronaut([-5.0, 2.4, 0], scale=0.7, tilt=0.3)
        station = make_station([-1.5, 2.6, 0], scale=0.6)
        earth = make_earth([3.5, 2.6, 0]).scale(1.4)

        elev = make_elevator(2.0, 2.6).move_to([-4.5, -1.0, 0])
        person = make_person(0.8).move_to([-4.7, -1.5, 0])
        scale = make_scale(0.8).move_to([-4.7, -2.1, 0])
        cable = make_cable([-4.5, 1.0, 0], [-4.5, 0.3, 0], broken=True)

        qm = question_mark([-1.0, -1.0, 0])
        bl = big_label("ZERO", [-1.0, -2.4, 0], size=48)
        sl = small_label("~8 km/s", [-1.0, 0.2, 0])

        limb = earth_limb([3.0, -7.5, 0], 6.0)
        arc = ballistic_arc([0.6, -0.8, 0], 1.6, g=4.0, t_max=1.6)
        carc = curved_fall_arc([3.0, -7.5, 0], 6.0, 2.2, 1.4, 0.8)
        orb = orbit_circle([3.0, -1.5, 0], 1.5)

        self.add(astro, station, earth, elev, person, scale, cable,
                 qm, bl, sl, limb, arc, carc, orb)
        self.wait(0.3)
