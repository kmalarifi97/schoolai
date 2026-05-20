from manim import *
import numpy as np
from fictitious_helpers import (rotating_disk, split_divider, frame_label,
                                BALL_COL, PATH_COL)

# "Nothing bent the ball's path through space—it went perfectly
#  straight. But the floor rotated beneath that straight path, so from
#  the floor it looks curved."
DUR = 12.1


class FictitiousS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(split_divider(0.0))

        LC = np.array([-3.5, -0.2, 0])
        RC = np.array([3.5, -0.2, 0])
        R = 2.1
        omega = PI * 0.7

        # LEFT: fixed space view — disk spins, ball goes dead straight
        ldisk = rotating_disk(LC, radius=R, n_spokes=8)
        # RIGHT: disk view — disk fixed, same path appears curved
        rdisk = rotating_disk(RC, radius=R, n_spokes=8)
        self.add(ldisk, rdisk)

        lcap = frame_label("space view", LC + np.array([0, 3.0, 0]),
                           size=24)
        rcap = frame_label("disk view", RC + np.array([0, 3.0, 0]),
                           size=24)
        self.add(lcap, rcap)

        lball = Dot(point=LC, radius=0.12, color=BALL_COL)
        rball = Dot(point=RC, radius=0.12, color=BALL_COL)
        ltrail = TracedPath(lball.get_center, stroke_color=PATH_COL,
                            stroke_width=4)
        rtrail = TracedPath(rball.get_center, stroke_color=PATH_COL,
                            stroke_width=4)
        self.add(lball, rball, ltrail, rtrail)

        end_off = np.array([0, R, 0])  # straight, radially outward (up)

        def lupd(mob, a):
            mob.move_to(LC + end_off * a)

        def rupd(mob, a):
            # same straight path, expressed in the rotating disk frame:
            # rotate the space position back by -omega*a
            p = end_off * a
            th = -omega * a
            x = p[0] * np.cos(th) - p[1] * np.sin(th)
            y = p[0] * np.sin(th) + p[1] * np.cos(th)
            mob.move_to(RC + np.array([x, y, 0]))

        self.play(
            UpdateFromAlphaFunc(lball, lupd),
            UpdateFromAlphaFunc(rball, rupd),
            Rotate(ldisk, angle=omega, about_point=LC),
            run_time=3.4, rate_func=rate_functions.linear)
        self.wait(DUR - 4.4)
