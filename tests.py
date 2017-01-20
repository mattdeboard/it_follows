import os.path as op
import unittest

from it_follows import route_to_dir


class TestFollower(unittest.TestCase):
    def test_route_to_dir(self):
        root = op.abspath(op.curdir)
        target = op.join(root, 'foo')
        destination = op.join(root, 'bar', 'baz', 'qux')
        self.assertEqual(route_to_dir(target, destination),
                         op.abspath(op.join(target, '..')))

        destination = op.join(root, 'foo')
        target = op.join(root, 'bar', 'baz', 'qux')
        self.assertEqual(route_to_dir(target, destination),
                         op.abspath(op.join(target, '..')))

        target = root
        destination = op.join(root, 'foo')
        self.assertEqual(route_to_dir(target, destination),
                         destination)
