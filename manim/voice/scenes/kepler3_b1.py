from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from grav_helpers import make_fabric_3d
from kepler3_helpers import make_sun, NEUTRAL, NEUTRAL_D, DIM

# "Last time, you saw the planets slide into their orbits — down the bend
#  in space. But look closer. Each planet keeps its own orbit, its own
#  year. Mercury, close in, races. Neptune, far out, crawls."
DUR = 15.6


class Kepler3S1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # Resume the teaser's curved-space bend.
        fabric = make_fabric_3d(dip_amount=1.0)
        self.play(Create(fabric), run_time=2.4, lag_ratio=0.02)
        sun = make_sun([0, -0.35, 0], scale=0.7)
        self.play(FadeIn(sun, scale=0.8), run_time=1.0)

        center = np.array([0, -0.35, 0])
        # Several planets: inner fast/tight, outer slow/wide.
        specs = [
            (1.1, 0.10, "#C9B07A", 1.0),    # Mercury — close, fast
            (1.9, 0.15, NEUTRAL, 0.62),
            (2.9, 0.18, "#9BD6B0", 0.40),
            (3.9, 0.13, "#7FA8E8", 0.26),   # Neptune — far, slow
        ]
        planets, rings = VGroup(), VGroup()
        for r, pr, col, _ in specs:
            ring_pts = []
            for i in range(101):
                ang = 2 * np.pi * i / 100
                ring_pts.append(center + np.array(
                    [r * np.cos(ang), r * 0.34 * np.sin(ang), 0]))
            ring = VMobject().set_points_smoothly(ring_pts)
            ring.set_stroke(DIM, width=1.6, opacity=0.4)
            rings.add(ring)
            p = Circle(radius=pr, fill_color=col, fill_opacity=1,
                       stroke_color=NEUTRAL_D, stroke_width=1.5)
            p.move_to(center + np.array([r, 0, 0]))
            planets.add(p)
        self.play(Create(rings), run_time=1.6)
        self.play(*[FadeIn(p, scale=0.7) for p in planets], run_time=1.0)

        # Each planet keeps its own pace — inner races, outer crawls.
        trackers = [ValueTracker(0.0) for _ in specs]
        for p, (r, pr, col, sp), tr in zip(planets, specs, trackers):
            def make_upd(r=r, sp=sp, tr=tr):
                def upd(m):
                    a = tr.get_value() * sp
                    m.move_to(center + np.array(
                        [r * np.cos(a), r * 0.34 * np.sin(a), 0]))
                return upd
            p.add_updater(make_upd())
        self.play(*[tr.animate.set_value(2 * np.pi) for tr in trackers],
                  run_time=DUR - 6.5, rate_func=linear)
        for p in planets:
            p.clear_updaters()
        self.wait(0.3)
