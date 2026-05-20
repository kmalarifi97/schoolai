from manim import *
import numpy as np
from springdrop_helpers import (
    make_yousef, make_spring, make_ball, make_bell, target_line,
    rise_path, energy_bar, energy_chain, ledger, slider,
    hanging_spring, masses_springs_panel, hold_hand,
    compression_control, run_counter, predict_vs_result,
    callback_bow, callback_book, callback_cart, callback_pendulum,
    small_label, qmark)


class SpringdropTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        sp = make_spring([-5.6, -1.0, 0], height=1.2, compress=0.3)
        ball = make_ball(sp["top"] + UP * 0.22, r=0.18)
        bell = make_bell([-5.6, 1.6, 0], scale=0.7)
        tl = target_line(1.4, x0=-6.2, x1=-4.8)
        you = make_yousef([-4.4, -0.8, 0], scale=0.6)
        rp = rise_path([-3.4, -1.6, 0], 1.2, color="#9BD6B0",
                       width=3)

        eb = VGroup(
            energy_bar("spring", 0.8, [-2.4, 1.2, 0], color="#7FB8E8",
                       max_h=1.6, w=0.4),
            energy_bar("speed", 0.4, [-1.8, 1.2, 0], color="#E8C46B",
                       max_h=1.6, w=0.4))
        ec = energy_chain([0.4, 1.4, 0], stage=0.5, scale=0.55)
        led = ledger([3.4, 1.4, 0], rows=3, scale=0.6)

        msp = masses_springs_panel([-2.6, -2.0, 0], stiffness=0.6,
                                    mass=0.5, elastic=0.6, kinetic=0.2,
                                    grav=0.1, scale=0.5)
        sl = slider([1.2, -1.0, 0], frac=0.5, w=1.8)
        hh = hold_hand([2.6, -1.0, 0], scale=0.7)
        cc = compression_control([1.8, -1.9, 0], frac=0.4)
        rc = run_counter([4.2, -1.0, 0], used=1, total=3)
        pvr = predict_vs_result([4.4, -2.6, 0], pred=0.4, res=0.7)

        bw = callback_bow([-4.6, 2.8, 0], scale=0.7)
        bk = callback_book([-2.6, 2.8, 0], scale=0.7)
        ct = callback_cart([-0.6, 2.9, 0], scale=0.7)
        pd = callback_pendulum([1.4, 3.0, 0], scale=0.7)
        q = qmark([3.4, 3.0, 0])

        self.add(sp["group"], ball, bell, tl, you, rp, eb, ec, led,
                 msp, sl, hh, cc, rc, pvr, bw, bk, ct, pd, q)
        self.wait(0.3)
