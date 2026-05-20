from manim import *
import numpy as np
from skatepark_helpers import (
    make_faris, make_ramp, board_dot, arc_path, ideal_arc,
    surface_swatch, plywood_stack, energy_bar, bar_chart_panel,
    phet_track, play_button, friction_slider, run_counter,
    predict_vs_result, callback_book, callback_cart, callback_pendulum,
    small_label, qmark)


class SkateparkTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        r = make_ramp(launch_h=2.0)
        ramp = r["group"].copy().scale(0.42).move_to([-4.4, 2.0, 0])
        ideal = ideal_arc(r["lip"], r["land_top"]).scale(0.42).move_to(
            [-4.4, 2.4, 0])
        faris = make_faris([-1.2, 2.2, 0], scale=0.7)
        arc1 = arc_path(r["lip"], r["land_lo"], peak=1.0, color="#C98A6B"
                        ).scale(0.4).move_to([1.4, 2.2, 0])
        sw_r = surface_swatch([4.6, 2.4, 0], waxed=False, w=2.4, h=0.5)
        sw_w = surface_swatch([4.6, 1.6, 0], waxed=True, w=2.4, h=0.5)

        stack = plywood_stack([-5.4, -1.2, 0], n=5, w=1.3)
        eb = VGroup(
            energy_bar("stored", 0.8, [-3.8, -1.4, 0], color="#7FB8E8"),
            energy_bar("speed", 0.5, [-3.0, -1.4, 0], color="#E8C46B"),
            energy_bar("heat", 0.2, [-2.2, -1.4, 0], color="#D98C5F"))
        panel = bar_chart_panel([-0.2, -1.4, 0], pe=0.6, ke=0.3, th=0.1,
                                scale=0.7)
        track = phet_track([2.4, -1.4, 0], launch_h=1.6, scale=0.7)
        pb = play_button([4.6, -0.6, 0], r=0.3)
        fs = friction_slider([4.6, -1.6, 0], frac=0.4, w=1.8)

        rc = run_counter([-4.8, -3.0, 0], used=1, total=3)
        pvr = predict_vs_result([-2.0, -3.0, 0], pred=0.4, res=0.7)
        bk = callback_book([1.2, -3.0, 0], scale=0.8)
        ct = callback_cart([2.8, -3.0, 0], scale=0.8)
        pd = callback_pendulum([4.4, -3.0, 0], scale=0.8)
        q = qmark([0, 3.4, 0])

        self.add(ramp, ideal, faris, arc1, sw_r, sw_w, stack, eb,
                 panel, track, pb, fs, rc, pvr, bk, ct, pd, q)
        self.wait(0.4)
