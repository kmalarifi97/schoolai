from manim import *
import numpy as np
from weightless_helpers import earth_limb, curved_fall_arc, orbit_circle, small_label

# "Throw it fast enough—about eight kilometers per second—and the ground
#  curves away beneath it just as fast as it falls. It keeps falling,
#  and never lands."
DUR = 12.5

CX, CY, R = 0.0, -2.4, 2.7


class WeightlessS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([CX, CY, 0])
        limb = earth_limb(C, R)
        self.play(FadeIn(limb), run_time=1.0)

        th0 = np.pi / 2
        # a long curving fall that wraps most of the way around
        partial = curved_fall_arc(C, R, th0, th0 - 4.4, 0.85,
                                  color="#E8C97F")
        self.play(Create(partial), run_time=2.4,
                  rate_func=rate_functions.linear)

        # speed indicator appears briefly
        spd = small_label("~8 km/s", C + np.array([0, R + 0.9, 0]),
                          color="#EAE4D5", size=28)
        self.play(FadeIn(spd, scale=0.7), run_time=0.8)

        # the arc closes into a full circle
        orbit = orbit_circle(C, R + 0.85, color="#E8C97F", width=4)
        self.play(FadeOut(partial), Create(orbit), run_time=2.2,
                  rate_func=rate_functions.ease_in_out_sine)
        ball = Dot(C + np.array([0, R + 0.85, 0]), radius=0.10,
                   color="#E8C97F")
        self.add(ball)
        self.play(MoveAlongPath(
            ball, orbit_circle(C, R + 0.85)), run_time=2.0,
            rate_func=rate_functions.linear)
        self.play(spd.animate.set_opacity(0.0), run_time=0.6)
        self.wait(DUR - 9.0)
