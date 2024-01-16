# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots["TestGrid::test_set 1"] = [
    [1, None, None],
    [None, 2, None],
    [None, None, 3],
    [None, None, 4],
]

snapshots["TestGridGenerator::test_identity grid_identity_3"] = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
]

snapshots["TestGridGenerator::test_identity hex_identity_5"] = [
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1],
]

snapshots["TestGridGenerator::test_identity matrix_identity_5"] = GenericRepr(
    "array([[1, 0, 0, 0, 0],\n       [0, 1, 0, 0, 0],\n       [0, 0, 1, 0, 0],\n       [0, 0, 0, 1, 0],\n       [0, 0, 0, 0, 1]])"
)
