from manim import *
import numpy as np
from collisionlab_helpers import (
    make_noura, make_brother, make_cart, table_line, clue_dent,
    clue_slide, clue_sound, momentum_bar, energy_bar, loss_shimmer,
    cl_track, cl_puck, momentum_arrow, ke_readout, play_button,
    mass_slider, run_counter, predict_vs_result, callback_cars_wall,
    callback_lake_throw, callback_steel_clay, small_label, qmark)


class CollisionlabTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        no = make_noura([-5.6, 2.4, 0], scale=0.7)
        br = make_brother([-4.4, 2.3, 0], scale=0.7)
        c1 = make_cart([-2.7, 2.5, 0], scale=0.7, color="#7FB8E8")
        c2 = make_cart([-1.2, 2.5, 0], scale=0.7, color="#E8C46B",
                       dented=True, facing=-1)
        cd = clue_dent([0.4, 2.5, 0], crossed=True)
        cs = clue_slide([1.7, 2.5, 0], crossed=True)
        cn = clue_sound([3.0, 2.5, 0], crossed=True)
        q = qmark([4.2, 2.5, 0])
        tbl = table_line(1.7)

        mb = momentum_bar([-3.2, 0.7, 0], length=4.0, split=0.4,
                          label="total p")
        eb = energy_bar("motion", 0.55, [-0.2, 0.7, 0])
        ls = loss_shimmer([2.6, 0.7, 0], scale=0.8)

        tr = cl_track([-2.4, -1.2, 0], w=5.0)
        p1 = cl_puck([-3.6, -1.2, 0], color="#7FB8E8", mass="2")
        p2 = cl_puck([-1.2, -1.2, 0], color="#E8C46B", mass="1")
        ar = momentum_arrow([-3.6, -1.2, 0], 0.8)
        ke = ke_readout([0.9, -1.0, 0], scale=0.7)
        pb = play_button([2.9, -1.1, 0], r=0.3)

        ms = mass_slider([-4.6, -3.0, 0], frac=0.4, w=1.8)
        rc = run_counter([-2.4, -3.0, 0], used=1, total=3)
        pvr = predict_vs_result([-0.2, -3.0, 0], pred=0.4, res=0.7)
        cw = callback_cars_wall([2.0, -3.0, 0], scale=0.8)
        lt = callback_lake_throw([3.8, -3.0, 0], scale=0.8)
        sc = callback_steel_clay([5.3, -3.0, 0], scale=0.8)
        sl = small_label("Collision Lab", [3.2, 1.7, 0], size=22)

        self.add(no, br, c1, c2, cd, cs, cn, q, tbl, mb, eb, ls, tr,
                 p1, p2, ar, ke, pb, ms, rc, pvr, cw, lt, sc, sl)
        self.wait(0.3)
