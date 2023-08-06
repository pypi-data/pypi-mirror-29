import sys; sys.path.append("../")

import unittest
import copy

from delimited.path import TuplePath
from delimited.path import DelimitedStrPath


class TestTuplePath(unittest.TestCase):

    # _encode

    def test___encode(self):
        a = TuplePath()
        self.assertEqual(a._encode(["k1", "k2", "k3"]), ("k1", "k2", "k3"))

    # _decode

    def test___decode(self):
        a = TuplePath()
        self.assertEqual(a._decode(("k1", "k2", "k3")), ["k1", "k2", "k3"])

    # __init__

    def test___init___no_params(self):
        a = TuplePath()
        self.assertEqual(a, ())

    def test___init___tuple_key_notation_param(self):
        a = TuplePath(("k1", "k2", "k3"))
        self.assertEqual(a, ("k1", "k2", "k3"))

    # __call__

    def test___call___no_params(self):
        a = TuplePath()
        a()
        self.assertEqual(a, ())

    def test___call___no_params__existing_segments(self):
        a = TuplePath()
        a.segments = ["foo", "bar", "baz"]
        a()
        self.assertEqual(a, ())

    def test___call___tuple_key_notation_param__existing_segments(self):
        a = TuplePath()
        a.segments = ["foo", "bar", "baz"]
        a(("k1", "k2", "k3"))
        self.assertEqual(a, ("k1", "k2", "k3"))

    # __add__

    def test___add__(self):
        a = TuplePath(("k1", "k2", "k3"))
        b = "k4"
        c = a + b
        self.assertIsInstance(c, TuplePath)
        self.assertEqual(c, ("k1", "k2", "k3", "k4"))

    # __iadd__

    def test___iadd____tuple_param(self):
        a = TuplePath(("k1", "k2", "k3"))
        b = "k4"
        a += b
        self.assertEqual(a, ("k1", "k2", "k3", "k4"))

    # __eq__

    def test___eq___same_class_param__returns_True(self):
        a = TuplePath(("k1", "k2", "k3"))
        b = TuplePath(("k1", "k2", "k3"))
        self.assertTrue(a == b)

    def test___eq___same_class_param__returns_False(self):
        a = TuplePath(("k1", "k2", "k3"))
        b = TuplePath(("foo", "bar", "baz"))
        self.assertFalse(a == b)

    def test___eq___tuple_param__returns_True(self):
        a = TuplePath(("k1", "k2", "k3"))
        b = ("k1", "k2", "k3")
        self.assertTrue(a == b)

    def test___eq___tuple_param__returns_False(self):
        a = TuplePath(("k1", "k2", "k3"))
        b = ("foo", "bar", "baz")
        self.assertFalse(a == b)

    def test___eq___incompatible_type__returns_False(self):
        a = TuplePath(("k1", "k2", "k3"))
        b = True
        self.assertFalse(a == b)

    # __ne__

    def test___ne___same_class_param__returns_False(self):
        a = TuplePath(("k1", "k2", "k3"))
        b = TuplePath(("k1", "k2", "k3"))
        self.assertFalse(a != b)

    def test___ne___same_class_param__returns_True(self):
        a = TuplePath(("k1", "k2", "k3"))
        b = TuplePath(("foo", "bar", "baz"))
        self.assertTrue(a != b)

    def test___ne___tuple_param__returns_False(self):
        a = TuplePath(("k1", "k2", "k3"))
        b = ("k1", "k2", "k3")
        self.assertFalse(a != b)

    def test___ne___tuple_param__returns_True(self):
        a = TuplePath(("k1", "k2", "k3"))
        b = ("foo", "bar", "baz")
        self.assertTrue(a != b)

    def test___ne___incompatible_type__returns_True(self):
        a = TuplePath(("k1", "k2", "k3"))
        b = Exception
        self.assertTrue(a != b)

    # __hash__

    def test___hash__(self):
        a = hash(TuplePath(("k1", "k2", "k3")))
        b = hash(TuplePath(("k1", "k2", "k3")))
        self.assertEqual(a, b)

    # __len__

    def test___len__(self):
        a = TuplePath()
        self.assertEqual(len(a), 0)

        b = TuplePath(("k1", "k2", "k3"))
        self.assertEqual(len(b), 3)

    # __str__

    def test___str__(self):
        a = TuplePath()
        self.assertEqual(str(a), "()")
        b = TuplePath(("k1", "k2", "k3"))
        self.assertEqual(str(b), "('k1', 'k2', 'k3')")

    # __repr__

    def test___repr__(self):
        a = TuplePath(("k1", "k2", "k3"))
        self.assertEqual(repr(a), "TuplePath(('k1', 'k2', 'k3'))")

    # __bool__

    def test___bool___returns_False(self):
        a = TuplePath()
        self.assertFalse(a)

    def test___bool___returns_True(self):
        a = TuplePath(("k1", "k2", "k3"))
        self.assertTrue(a)

    # __iter__

    def test___iter__(self):
        a = TuplePath(("k1", "k2", "k3"))
        self.assertEqual(list(iter(a)), ["k1", "k2", "k3"])

    # __reversed__

    def test___reversed__(self):
        a = TuplePath(("k1", "k2", "k3"))
        self.assertEqual(list(reversed(a)), ["k3", "k2", "k1"])

    # __contains__

    def test___contains____returns_True(self):
        a = TuplePath(("k1", "k2", "k3"))
        self.assertTrue("k2" in a)

    def test___contains____returns_False(self):
        a = TuplePath(("k1", "k2", "k3"))
        self.assertFalse("foo" in a)

    # __getitem__

    def test___getitem__int_index(self):
        a = TuplePath(("k3", "k2", "k1"))
        self.assertEqual(a[1], "k2")

    def test___getitem__slice_index(self):
        a = TuplePath(("k3", "k2", "k1"))
        self.assertEqual(a[:-1], ("k3", "k2"))

    # __setitem__

    def test___setitem__int_index(self):
        a = TuplePath(("k1", "k2", "k3"))
        a[1] = "foo"
        self.assertEqual(a, ("k1", "foo", "k3"))

    def test___setitem__slice_index(self):
        a = TuplePath(("k1", "k2", "k3"))
        a[:-1] = ("foo", "bar")
        self.assertEqual(a, ("foo", "bar", "k3"))

    # __delitem__

    def test___delitem__int_index(self):
        a = TuplePath(("k1", "k2", "k3"))
        del a[1]
        self.assertEqual(a, ("k1", "k3"))

    def test___delitem__slice_index(self):
        a = TuplePath(("k1", "k2", "k3"))
        del a[:-1]
        self.assertEqual(a, ("k3",))

    # append

    def test_append__str_param(self):
        a = TuplePath()
        self.assertEqual(a, ())
        a.append("k1")
        self.assertEqual(a, ("k1",))
        a.append("k2")
        self.assertEqual(a, ("k1", "k2"))

    # extend

    def test_extend__same_class(self):
        a = TuplePath(("k1",))
        b = TuplePath(("k2",))
        a.extend(b)
        self.assertEqual(a, ("k1", "k2"))

    def test_extend__external_representation(self):
        a = TuplePath(("k1",))
        b = ("k2",)
        a.extend(b)
        self.assertEqual(a, ("k1", "k2"))

    # insert

    def test_insert(self):
        a = TuplePath(("k2",))
        a.insert(1, "k3")
        self.assertEqual(a, ("k2", "k3"))
        a.insert(0, "k1")
        self.assertEqual(a, ("k1", "k2", "k3"))

    # remove

    def test_remove(self):
        a = TuplePath(("k1", "k2", "k3"))
        a.remove("k2")
        self.assertEqual(a, ("k1", "k3"))

    # pop

    def test_pop(self):
        a = TuplePath(("k1", "k2", "k3"))
        self.assertEqual(a.pop(), "k3")
        self.assertEqual(a, ("k1", "k2"))
        self.assertEqual(a.pop(0), "k1")
        self.assertEqual(a, ("k2",))

    # clear

    def test_clear(self):
        a = TuplePath(("k1", "k2", "k3"))
        a.clear()
        self.assertEqual(a, ())

    # index

    def test_index(self):
        a = TuplePath(("k1", "k2", "k3"))
        self.assertEqual(a.index("k2"), 1)

    # count

    def test_count(self):
        a = TuplePath(("k1", "k1", "k2"))
        self.assertEqual(a.count("k1"), 2)

    # reverse

    def test_reverse(self):
        a = TuplePath(("k1", "k2", "k3"))
        a.reverse()
        self.assertEqual(a, ("k3", "k2", "k1"))

    # copy

    def test_copy(self):
        a = TuplePath(("k1", "k2", "k3"))
        b = a.copy()
        self.assertIsNot(a, b)
        self.assertEqual(a, b)
        a[1] = "foo"
        self.assertEqual(a, ("k1", "foo", "k3"))
        self.assertNotEqual(a, b)
        
    def test_copy__index_set(self):
        a = TuplePath(("k1", "k2", "k3"))
        b = a.copy(slice(1, len(a)))
        self.assertEqual(b, ("k2", "k3"))
        
    # clone
    
    def test_clone(self):
        a = TuplePath(("k1", "k2", "k3"))
        b = a.clone()
        self.assertIsNot(a, b)
        self.assertEqual(a, b)
        a[1] = "foo"
        self.assertEqual(a, ("k1", "foo", "k3"))
        self.assertEqual(b, ("k1", "foo", "k3"))
        self.assertEqual(a, b)

    # encode

    def test_encode(self):
        a = TuplePath(("k1", "k2", "k3"))
        b = a.encode()
        self.assertIsInstance(b, tuple)
        self.assertEqual(b, ("k1", "k2", "k3"))


class TestDelimitedStrPath(unittest.TestCase):

    # _encode

    def test___encode(self):
        a = DelimitedStrPath()
        self.assertEqual(a._encode(["k1", "k2", "k3"]), "k1.k2.k3")

    # _decode

    def test___decode(self):
        a = DelimitedStrPath()
        self.assertEqual(a._decode("k1.k2.k3"), ["k1", "k2", "k3"])
        
    # __repr__
    
    def test____repr__(self):
        a = DelimitedStrPath()
        self.assertEqual(repr(a), "DelimitedStrPath('')")
        
        a("k1.k2.k3")
        self.assertEqual(repr(a), "DelimitedStrPath('k1.k2.k3')")


if __name__ == "__main__":
    unittest.main()
