from manim import *
import numpy as np
from thermalbudget_helpers import (
    make_maha, make_heater, ice_on_heater, metal_cup, countdown_timer,
    thermometer, energy_ledger, temp_energy_curve, efc_layout,
    play_button, heat_rate_control, run_counter, predict_vs_result,
    target_dotted, callback_match_tub, callback_water_oil,
    callback_transfer, callback_stuck_thermo, small_label, qmark)


class ThermalbudgetTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        ice = ice_on_heater([-5.3, 2.4, 0], scale=0.5, heat=0.7,
                             melt=0.3)
        cup = metal_cup([-3.6, 2.4, 0], scale=0.6, heat=0.6, fill=0.5)
        tmr = countdown_timer([-2.0, 2.5, 0], scale=0.6, frac=0.4)
        th = thermometer([-0.7, 2.3, 0], scale=0.5, level=40)
        maha = make_maha([0.4, 2.3, 0], scale=0.7)
        led = energy_ledger(
            [("raise temp", 0.4, "#D98C5F"),
             ("hidden melt", 0.85, "#9BD6B0"),
             ("delivery rate", 0.5, "#B9BFC6")],
            [3.8, 2.4, 0], scale=0.5, title="thermal budget")

        crv = temp_energy_curve([-3.6, -0.4, 0], scale=0.55,
                                progress=1.0)
        efc = efc_layout([0.5, -0.5, 0], scale=0.55, heat=0.6,
                         melt=0.3)
        pb = play_button([3.0, -0.3, 0], r=0.3)
        hr = heat_rate_control([4.6, -0.3, 0], frac=0.5, w=1.8)
        rc = run_counter([4.6, -1.4, 0], used=1, total=3)

        tg = target_dotted([-4.6, -2.9, 0], scale=0.5)
        cm = callback_match_tub([-1.6, -2.9, 0], scale=0.45)
        cw = callback_water_oil([0.9, -2.9, 0], scale=0.5)
        ct = callback_transfer([3.6, -2.9, 0], scale=0.42)
        cs = callback_stuck_thermo([5.6, -1.2, 0], scale=0.45)
        q = qmark([0, 3.6, 0])

        self.add(ice, cup, tmr, th, maha, led, crv, efc, pb, hr,
                 rc, tg, cm, cw, ct, cs, q)
        self.wait(0.3)
