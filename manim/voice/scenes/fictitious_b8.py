from manim import *
import numpy as np
from fictitious_helpers import rotating_disk, frame_label, BALL_COL, PATH_COL

# "From above, it goes perfectly straight. From on the platform, it
#  curves away — and misses."
DUR = 7.8


class FictitiousS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, -0.2, 0])
        disk = rotating_disk(C, radius=2.7, n_spokes=8)
        # dim the bright reference spoke so the ball path reads clearest
        disk[2].set_stroke(color="#5A6E80", width=2).set_opacity(0.45)
        self.add(disk)

        # the friend starts at the right edge; the ball is aimed there
        target0 = C + np.array([2.55, 0, 0])
        friend = Dot(point=target0, radius=0.20, color="#E8C46A")
        self.add(friend)

        ball = Dot(point=C, radius=0.14, color=BALL_COL)
        trail = TracedPath(ball.get_center, stroke_color=PATH_COL,
                           stroke_width=6)
        self.add(ball, trail)

        # ball travels straight in space toward where the friend WAS,
        # while the disk spins the friend away from that line. From
        # above the path is a straight radial line; the friend has
        # moved on, so the ball sails past where they used to be.
        omega = PI * 0.55
        end = C + np.array([2.55, 0, 0])

        def upd(mob, alpha):
            mob.move_to(C + (end - C) * alpha)
        self.play(
            UpdateFromAlphaFunc(ball, upd),
            Rotate(disk, angle=omega, about_point=C),
            Rotate(friend, angle=omega, about_point=C),
            run_time=2.6, rate_func=rate_functions.linear)

        miss = frame_label("misses", end + np.array([0.15, 0.55, 0]),
                           color=PATH_COL, size=24)
        gap = DashedLine(end, friend.get_center(), color="#E07A5F",
                         stroke_width=3, dash_length=0.12).set_opacity(0.8)
        self.play(Create(gap), FadeIn(miss), run_time=0.9)
        self.wait(DUR - 3.4)
