"""
Unit tests for feature_shapes.py.

"""

import unittest
from bioplotlib.feature_shapes import *
import numpy as np

from matplotlib.path import Path
from matplotlib.patches import PathPatch


class TestRectangle(unittest.TestCase):

    def test_simple(self):
        obj = Rectangle(start=1, end=3, offset=1, width=1, by_axis="x")

        expected_verts = [
            [1., 1.],
            [1., 2.],
            [3., 2.],
            [3., 1.],
            [1., 1.]
            ]

        expected_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_by_axis_y(self):
        obj = Rectangle(start=1, end=3, offset=1, width=1, by_axis="y")

        expected_verts = [
            [1., 1.],
            [2., 1.],
            [2., 3.],
            [1., 3.],
            [1., 1.]
            ]

        expected_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_offset(self):
        obj = Rectangle(start=1, end=2, offset=1, width=1, by_axis="x")

        expected_verts = [
            [1., 1.],
            [1., 2.],
            [2., 2.],
            [2., 1.],
            [1., 1.]
            ]

        expected_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_path(self):
        obj = Rectangle(start=1, end=2, offset=1, width=1, by_axis="y")

        self.assertIsInstance(obj.path, Path)


class TestTriangle(unittest.TestCase):

    def test_simple(self):
        obj = Triangle(start=1, end=3, offset=1, width=1, by_axis="x")

        expected_verts = [
            [1., 1.],
            [1., 2.],
            [3., 1.5],
            [1., 1.]
            ]

        expected_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_by_axis_y(self):
        obj = Triangle(start=1, end=3, offset=1, width=1, by_axis="y")

        expected_verts = [
            [1., 1.],
            [2., 1.],
            [1.5, 3.],
            [1., 1.]
            ]

        expected_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_offset(self):
        obj = Triangle(start=1, end=2, offset=1, width=1, by_axis="x")

        expected_verts = [
            [1., 1.],
            [1., 2.],
            [2., 1.5],
            [1., 1.]
            ]

        expected_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_path(self):
        obj = Triangle(start=1, end=2, offset=1, width=1, by_axis="y")

        self.assertIsInstance(obj.path, Path)


class TestArrow(unittest.TestCase):

    def test_simple(self):
        obj = Arrow(start=1, end=3, offset=1, width=1, by_axis="x")

        expected_verts = [
            [1., 1.],
            [1., 2.],
            [2., 2.],
            [2., 2.],
            [3., 1.5],
            [2., 1.],
            [2., 1.],
            [1., 1.]
            ]

        expected_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_by_axis_y(self):
        obj = Arrow(start=1, end=3, offset=1, width=1, by_axis="y")

        expected_verts = [
            [1., 1.],
            [2., 1.],
            [2., 2.],
            [2., 2.],
            [1.5, 3.],
            [1., 2.],
            [1., 2.],
            [1, 1.]
            ]

        expected_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_offset(self):
        obj = Arrow(start=0, end=2, offset=1, width=1, by_axis="x")

        expected_verts = [
            [0., 1.],
            [0., 2.],
            [1., 2.],
            [1., 2.],
            [2., 1.5],
            [1., 1.],
            [1., 1.],
            [0., 1.]
            ]

        expected_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_tail_width(self):
        obj = Arrow(start=0,
                    end=2,
                    offset=0,
                    width=1,
                    tail_width=0.5,
                    head_length=1,
                    by_axis="x")

        expected_verts = [
            [0., 0.25],
            [0., 0.75],
            [1., 0.75],
            [1., 1.],
            [2., 0.5],
            [1., 0.],
            [1., 0.25],
            [0., 0.25]
            ]

        expected_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_head_length(self):
        obj = Arrow(start=0,
                    end=2,
                    offset=0,
                    width=1,
                    tail_width=0.5,
                    head_length=1.5,
                    by_axis="x")

        expected_verts = [
            [0., 0.25],
            [0., 0.75],
            [0.5, 0.75],
            [0.5, 1.],
            [2., 0.5],
            [0.5, 0.],
            [0.5, 0.25],
            [0., 0.25]
            ]

        expected_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_patch(self):
        obj = Arrow(start=1, end=2, offset=1, width=1, by_axis="y")

        self.assertIsInstance(obj.path, Path)


class TestOpenTriangle(unittest.TestCase):

    def test_simple(self):
        obj = OpenTriangle(start=1, end=3, offset=1, width=1, by_axis="x")

        expected_verts = [
            [1., 1.],
            [2., 2.],
            [3., 1.],
            ]

        expected_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_by_axis_y(self):
        obj = OpenTriangle(start=1, end=3, offset=1, width=1, by_axis="y")

        expected_verts = [
            [1., 1.],
            [2., 2.],
            [1., 3.],
            ]

        expected_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_offset(self):
        obj = OpenTriangle(start=0, end=2, offset=1, width=1, by_axis="x")

        expected_verts = [
            [0., 1.],
            [1., 2.],
            [2., 1.],
            ]

        expected_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_patch(self):
        obj = OpenTriangle(start=1, end=2, offset=1, width=1, by_axis="y")

        self.assertIsInstance(obj.path, Path)


class TestOpenRectangle(unittest.TestCase):

    def test_simple(self):
        obj = OpenRectangle(start=1, end=3, offset=1, width=1, by_axis="x")

        expected_verts = [
            [1., 1.],
            [1., 2.],
            [3., 2.],
            [3., 1.],
            ]

        expected_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_by_axis_y(self):
        obj = OpenRectangle(start=1, end=3, offset=1, width=1, by_axis="y")

        expected_verts = [
            [1., 1.],
            [2., 1.],
            [2., 3.],
            [1., 3.],
            ]

        expected_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_offset(self):
        obj = OpenRectangle(start=0, end=2, offset=1, width=1, by_axis="x")

        expected_verts = [
            [0., 1.],
            [0., 2.],
            [2., 2.],
            [2., 1.],
            ]

        expected_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_patch(self):
        obj = OpenRectangle(start=1, end=2, offset=1, width=1, by_axis="y")

        self.assertIsInstance(obj.path, Path)


class TestOpenSemicircle(unittest.TestCase):

    def test_simple(self):
        obj = OpenSemicircle(start=1, end=3, offset=1, width=1, by_axis="x")

        expected_verts = [
            [1., 1.],
            [1., 2.],
            [3., 2.],
            [3., 1.],
            ]

        expected_codes = [
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_by_axis_y(self):
        obj = OpenSemicircle(start=1, end=3, offset=1, width=1, by_axis="y")

        expected_verts = [
            [1., 1.],
            [2., 1.],
            [2., 3.],
            [1., 3.],
            ]

        expected_codes = [
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_offset(self):
        obj = OpenSemicircle(start=0, end=2, offset=1, width=1, by_axis="x")

        expected_verts = [
            [0., 1.],
            [0., 2.],
            [2., 2.],
            [2., 1.],
            ]

        expected_codes = [
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            ]

        self.assertEqual(obj.vertices.tolist(), expected_verts)
        self.assertEqual(obj.codes, expected_codes)

    def test_patch(self):
        obj = OpenSemicircle(start=1, end=2, offset=1, width=1, by_axis="y")

        self.assertIsInstance(obj.path, Path)


if __name__ == '__main__':
    unittest.main()
