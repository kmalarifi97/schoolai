from manim import *
import numpy as np
from orbitlab_helpers import (
    make_planet, make_moon, moon_dot, gravity_arrow, straight_arrow,
    spiral_in_path, closed_circle_path, escape_path, radial_fall_path,
    dotted_circle, ellipse_path, curved_ground_inset,
    gravity_orbits_panel, make_controls, play_button, velocity_control,
    run_counter, callback_rocks, callback_field, callback_thrown,
    small_label, qmark)


class OrbitlabTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        c = np.array([-4.6, 2.0, 0])
        planet = make_planet(c, r=0.38)
        moon = make_moon(c + np.array([1.0, 0, 0]), r=0.10)
        ga = gravity_arrow(c + np.array([1.0, 0, 0]), c, length=0.5)
        sa = straight_arrow(c + np.array([1.0, 0, 0]), [0, 1, 0],
                            length=0.5)
        sp = spiral_in_path(c, r0=1.0, r_end=0.4).scale(0.6).move_to(
            [-2.4, 2.2, 0])
        cc = closed_circle_path(c, r=0.8).scale(0.6).move_to(
            [-0.6, 2.2, 0])
        ep = escape_path(c, r0=0.7).scale(0.6).move_to([1.4, 2.2, 0])
        dc = dotted_circle(c, r=0.8).scale(0.6).move_to([3.2, 2.2, 0])
        el = ellipse_path(c, a=1.0, b=0.6).scale(0.6).move_to(
            [5.0, 2.2, 0])

        inset = curved_ground_inset([-4.6, -0.4, 0], scale=0.7)
        gp = gravity_orbits_panel([-1.6, -0.4, 0], scale=0.55)
        ctrl = make_controls([1.8, -0.4, 0], scale=0.7)
        pb = play_button([4.4, 0.4, 0], r=0.3)
        vc = velocity_control([4.6, -0.8, 0], frac=0.4, w=1.8)

        rc = run_counter([-5.0, -3.0, 0], used=1, total=3)
        cr = callback_rocks([-2.4, -3.0, 0], scale=0.55)
        cf = callback_field([0.6, -3.0, 0], scale=0.55)
        ct = callback_thrown([3.4, -3.0, 0], scale=0.55)
        q = qmark([5.4, -3.0, 0])
        lbl = small_label("orbitlab", [0, 3.5, 0], color="#8C8576",
                          size=22)

        self.add(planet, moon, ga, sa, sp, cc, ep, dc, el, inset, gp,
                 ctrl, pb, vc, rc, cr, cf, ct, q, lbl)
        self.wait(0.3)
