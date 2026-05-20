from manim import *
import numpy as np
from rotke_helpers import make_ball, make_slope, energy_bar, small_label

# "A rolling ball carries both kinds at once — moving forward and
#  spinning. Two energies in one body."
DUR = 8.6


class RotkeS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        ln, start, end = make_slope(width=7.4, drop=3.0, base_y=-2.7,
                                    x0=-4.0)
        self.play(Create(ln), run_time=0.9)

        R = 0.42
        ball = make_ball(radius=R)
        # place tangent to the slope at the top
        slope_dir = (end - start) / np.linalg.norm(end - start)
        normal = np.array([-slope_dir[1], slope_dir[0], 0])
        p0 = start + slope_dir * 0.5 + normal * R
        ball.move_to(p0)
        self.play(FadeIn(ball, scale=0.6), run_time=0.7)

        # two bars riding along, both growing as it speeds up
        fwd_base = np.array([-5.4, -1.0, 0])
        spin_base = np.array([5.4, -1.0, 0])
        fb = energy_bar(0.02, fwd_base, width=0.45, color="#7FD6A5")
        sb = energy_bar(0.02, spin_base, width=0.45, color="#9CC4E0")
        self.add(fb, sb)
        self.add(small_label("forward motion",
                             fwd_base + np.array([0, -0.4, 0]),
                             size=20, color="#7FD6A5"))
        self.add(small_label("spin",
                             spin_base + np.array([0, -0.4, 0]),
                             size=20, color="#9CC4E0"))

        p1 = end + slope_dir * (-0.5) + normal * R
        dist = np.linalg.norm(p1 - p0)

        prev = [p0.copy()]

        def roll(m, dt):
            c = m.get_center()
            moved = np.linalg.norm(c - prev[0])
            if moved > 1e-6:
                m.rotate(-moved / R, about_point=c)
            prev[0] = c.copy()
        ball.add_updater(roll)

        self.play(
            ball.animate.move_to(p1),
            Transform(fb, energy_bar(2.4, fwd_base, width=0.45,
                                     color="#7FD6A5")),
            Transform(sb, energy_bar(1.7, spin_base, width=0.45,
                                     color="#9CC4E0")),
            run_time=2.6, rate_func=rate_functions.ease_in_quad)
        ball.clear_updaters()
        self.add(small_label("two energies in one body",
                             [0, -3.4, 0], size=24, color="#8C98A6"))
        self.wait(DUR - 6.2)
