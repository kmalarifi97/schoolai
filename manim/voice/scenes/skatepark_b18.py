from manim import *
import numpy as np
from skatepark_helpers import phet_track, bar_chart_panel, board_dot

# "Then he presses play. And he watches the bars, not the skater."
DUR = 6.0


class SkateparkS1B18(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        track = phet_track([-3.0, 0.2, 0], launch_h=1.6, scale=0.8)
        self.add(track)
        panel = bar_chart_panel([2.6, 0.0, 0], pe=0.85, ke=0.05,
                                th=0.0, scale=1.0)
        self.add(panel)
        self.wait(0.5)

        # the skater (a faint dot) runs along the track, attention on bars
        pts = track.track_pts
        dot = board_dot(pts[0], r=0.09).set_opacity(0.4)
        self.add(dot)

        # PE shrinks, KE rises, thermal creeps up, total stays flat
        new_panel = bar_chart_panel([2.6, 0.0, 0], pe=0.08, ke=0.70,
                                    th=0.07, scale=1.0)

        path = VMobject().set_points_smoothly(pts)
        self.play(
            MoveAlongPath(dot, path),
            Transform(panel, new_panel),
            run_time=3.0, rate_func=rate_functions.ease_in_out_sine)
        self.wait(DUR - 3.5)
