from manim import *
import numpy as np
from thermolaws_helpers import (
    stone_tablet, tablet_inscribe, tablet_arrow, energy_bar, engine_box,
    efficiency_dial, balance_scale, make_beaker, ink_blobs, coffee_mug,
    scatter_field, entropy_bar, time_arrow, never_stamp, cross_out,
)


class ThermolawsTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        t1 = stone_tablet([-5.6, 2.0, 0], scale=0.55, faint=False)
        ins = tablet_inscribe(t1, "energy is\nconserved", "I")
        t2 = stone_tablet([-5.6, -2.0, 0], scale=0.55, faint=False)
        arr = tablet_arrow(t2)

        eb = energy_bar([-1.5, 3.0, 0], total_width=3.6, height=0.4)
        eng = engine_box([-2.0, 0.3, 0], scale=0.7, dial_pct=58)
        bal = balance_scale([3.0, 1.8, 0], tilt=0.0, scale=0.7)

        bk, bc = make_beaker([5.0, 2.0, 0], scale=0.6)
        ink = ink_blobs(bc + [0, 0.3, 0], spread=0.6)

        mug = coffee_mug([1.4, -2.3, 0], scale=0.7, temp=1.0)
        sc = scatter_field([3.4, -2.0, 0], disorder=0.7, n_side=4, gap=0.3)
        ent = entropy_bar([5.5, -3.0, 0], frac=0.6, height=2.0)
        ta = time_arrow([0, -3.5, 0], length=3.0)
        nv = never_stamp([-3.5, -3.0, 0], scale=0.7)

        self.add(t1, ins, t2, arr, eb, eng, bal, bk, ink, mug, sc, ent,
                 ta, nv)
        self.add(cross_out(mug))
        self.wait(0.4)
