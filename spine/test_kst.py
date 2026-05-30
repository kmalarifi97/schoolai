#!/usr/bin/env python3
"""Unit tests for the KST engine. Run BEFORE wiring the backend (Phase 5 gate).

    python3 spine/test_kst.py

The canonical test is the 5-node chain from the build prompt:
    Function -> Derivative -> Velocity -> Momentum -> Conservation
A simulated student who knows Function + Derivative but not Velocity must be
located with the gap at Velocity.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kst  # noqa: E402

CHAIN = [
    {"from": "Function", "to": "Derivative", "type": "prerequisite"},
    {"from": "Derivative", "to": "Velocity", "type": "prerequisite"},
    {"from": "Velocity", "to": "Momentum", "type": "prerequisite"},
    {"from": "Momentum", "to": "Conservation", "type": "prerequisite"},
]
ORDER = ["Function", "Derivative", "Velocity", "Momentum", "Conservation"]


def _passed(name):
    print(f"  PASS  {name}")


def test_structure_is_a_chain():
    s = kst.knowledge_states(CHAIN, nodes=ORDER)
    # A 5-node chain has exactly 6 states: the prefixes {} .. full.
    assert len(s.states) == 6, f"expected 6 states, got {len(s.states)}"
    sizes = sorted(len(K) for K in s.states)
    assert sizes == [0, 1, 2, 3, 4, 5], sizes
    # Every state is a prefix of the chain (downward closed).
    for K in s.states:
        idxs = sorted(ORDER.index(n) for n in K)
        assert idxs == list(range(len(K))), f"{K} is not a prefix (not downward closed)"
    assert s.depth == {"Function": 0, "Derivative": 1, "Velocity": 2,
                       "Momentum": 3, "Conservation": 4}
    _passed("structure: 5-node chain -> 6 nested states, correct depths")


def _simulate(true_state, items, calib, seed_bits):
    """Deterministic simulated answers (no RNG): correct iff p_correct >= 0.5,
    i.e. the student reliably answers per BLIM expectation."""
    responses = []
    for item_id, node in items.items():
        p = kst.p_correct(node in true_state, calib[item_id]["slip"],
                          calib[item_id]["guess"])
        responses.append((item_id, p >= 0.5))
    return responses


def test_locates_velocity_gap():
    s = kst.knowledge_states(CHAIN, nodes=ORDER)
    # One clean item per node.
    items = {f"it-{n}": n for n in ORDER}
    calib = {i: {"slip": 0.10, "guess": 0.10} for i in items}  # low guess: informative
    # Ground truth: student knows Function + Derivative only.
    true_state = frozenset({"Function", "Derivative"})
    responses = _simulate(true_state, items, calib, None)

    g = kst.locate_gap(s, responses, items, calib)
    assert g["map_state"] == true_state, f"MAP {set(g['map_state'])} != {set(true_state)}"
    assert g["primary_gap"] == "Velocity", f"gap {g['primary_gap']} != Velocity"
    assert g["fringe"] == ["Velocity"], g["fringe"]
    # Mastery should be high for known, low for unknown.
    assert g["mastery"]["Derivative"] > 0.8 and g["mastery"]["Momentum"] < 0.2
    _passed("assessment: knows Function+Derivative -> gap located at Velocity")


def test_full_mastery_has_no_gap():
    s = kst.knowledge_states(CHAIN, nodes=ORDER)
    items = {f"it-{n}": n for n in ORDER}
    calib = {i: {"slip": 0.10, "guess": 0.10} for i in items}
    true_state = frozenset(ORDER)
    responses = _simulate(true_state, items, calib, None)
    g = kst.locate_gap(s, responses, items, calib)
    assert g["map_state"] == frozenset(ORDER)
    assert g["primary_gap"] is None and g["fringe"] == []
    _passed("assessment: full mastery -> no gap (fringe empty)")


def test_next_item_is_informative():
    s = kst.knowledge_states(CHAIN, nodes=ORDER)
    items = {f"it-{n}": n for n in ORDER}
    calib = {i: {"slip": 0.10, "guess": 0.10} for i in items}
    # With no responses yet, the half-split rule should pick a mid-chain item
    # (the most uncertain), not a chain endpoint.
    nxt = kst.next_item(s, [], items, calib)
    assert nxt in {"it-Velocity", "it-Derivative", "it-Momentum"}, nxt
    _passed(f"questioning: first half-split item = {nxt} (mid-structure)")


def test_unresolved_items_are_ignored():
    s = kst.knowledge_states(CHAIN, nodes=ORDER)
    items = {f"it-{n}": n for n in ORDER}
    items["it-noise"] = None  # unresolved item carries no node
    calib = {i: {"slip": 0.10, "guess": 0.10} for i in items}
    true_state = frozenset({"Function", "Derivative"})
    responses = [(i, kst.p_correct(items[i] in true_state if items[i] else False,
                                   0.10, 0.10) >= 0.5) for i in items if items[i]]
    responses.append(("it-noise", False))  # should not affect the result
    g = kst.locate_gap(s, responses, items, calib)
    assert g["primary_gap"] == "Velocity"
    _passed("robustness: unresolved (node=None) items ignored, gap still Velocity")


if __name__ == "__main__":
    print("KST engine tests (Phase 5 gate)")
    test_structure_is_a_chain()
    test_locates_velocity_gap()
    test_full_mastery_has_no_gap()
    test_next_item_is_informative()
    test_unresolved_items_are_ignored()
    print("ALL TESTS PASSED")
