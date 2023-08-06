import sys; sys.path.append("../")

import unittest
import copy

from delimited.path import TuplePath
from delimited.path import DelimitedStrPath

from delimited import NestedDict


class TestNestedDict(unittest.TestCase):

    # __init__

    def test___init__(self):
        a = NestedDict()
        self.assertEqual(a.data, {})
    
    def test___init____data_arg(self):
        a = NestedDict({"k": {"k": "v"}})
        self.assertEqual(a, {"k": {"k": "v"}})
        
    def test___init____raises_TypeError(self):
        with self.assertRaises(TypeError):
            a = NestedDict("foo")
    
    # __call__
    
    def test___call__(self):
        a = NestedDict({"k": {"k": "v"}})
        a()
        self.assertEqual(a, {})
    
    def test___call____data_arg(self):
        a = NestedDict()
        a({"k": {"k": "v"}})
        self.assertEqual(a, {"k": {"k": "v"}})
    
    # __bool__
    
    def test___bool____return_False(self):
        self.assertFalse(bool(NestedDict()))
    
    def test___bool____return_True(self):
        self.assertTrue(bool(NestedDict({"k": {"k": "v"}})))
    
    # __repr__
    
    def test___repr__(self):
        a = NestedDict({"k": {"k": "v"}})
        self.assertEqual(repr(a), "NestedDict({'k': NestedDict({'k': 'v'})})")
    
    # __eq__
    
    def test___eq____return_True(self):
        a1 = NestedDict({"k": {"k": "v"}})
        a2 = NestedDict({"k": {"k": "v"}})
        self.assertTrue(a1 == a2)
    
    def test___eq____return_False(self):
        a1 = NestedDict()
        a2 = None
        self.assertFalse(a1 == a2)
    
    def test___eq____same_class__return_False(self):
        a1 = NestedDict({"k": {"foo": "bar"}})
        a2 = NestedDict({"k": {"bar": "baz"}})
        self.assertFalse(a1 == a2)
    
    def test___eq____different_class__return_True(self):
        a1 = NestedDict({"k": {"foo": "bar"}})
        a2 = {"k": {"foo": "bar"}}
        self.assertTrue(a1 == a2)
    
        a3 = NestedDict()
        a4 = {}
        self.assertTrue(a3 == a4)
    
    # __ne__
    
    def test___ne____return_True(self):
        a1 = NestedDict({"k": {"foo": "bar"}})
        a2 = NestedDict({"k": {"bar": "baz"}})
        self.assertTrue(a1 != a2)
    
    def test___ne____return_False(self):
        a1 = NestedDict({"k": {"foo": "bar"}})
        a2 = NestedDict({"k": {"foo": "bar"}})
        self.assertFalse(a1 != a2)
    
    # __str__
    
    def test___str__(self):
        a = NestedDict({"foo": "bar"})
        self.assertEqual(str(a), "{'foo': 'bar'}")
    
    # __hash__
    
    def test___hash__(self):
        a1 = hash(NestedDict({"k": {"foo": "bar"}}))
        a2 = hash(NestedDict({"k": {"foo": "bar"}}))
        self.assertTrue(a1 == a2)
    
    # __iter__
    
    def test___iter__(self):
        a = NestedDict({"k1": "v", "k2": "v", "k3": "v"})
        for k, v in a:
            self.assertTrue(k in ["k1", "k2", "k3"])
            self.assertEqual(v, "v")
    
    # __contains__
    
    def test___contains__(self):
        a = NestedDict({"k1": "v", "k2": "v", "k3": "v"})
        self.assertTrue("k1" in a)
    
    # __getitem__
    
    def test___getitem__(self):
        a = NestedDict({"k": {"k": "v"}})
        self.assertEqual(a["k"], {"k": "v"})
    
    # __setitem__
    
    def test___setitem__(self):
        a = NestedDict({"k": {"foo": "bar"}})
        a["k"] = {"bar": "baz"}
        self.assertEqual(a.data, {"k": {"bar": "baz"}})
    
    # __delitem__
    
    def test___delitem__(self):
        a = NestedDict({"k": {"k": "v"}})
        del a["k"]
        self.assertEqual(a.data, {})

    # __len__
    
    def test___len__(self):
        a = NestedDict({"k1": "v", "k2": "v", "k3": "v"})
        self.assertEqual(len(a), 3)
    
    # __copy__
    
    def test___copy__(self):
        a1 = NestedDict({"k": {"foo": "bar"}})
        a2 = copy.copy(a1)
        self.assertIsNot(a1, a2)
        self.assertEqual(a1, a2)
        a1.data["k"]["foo"] = "baz"
        self.assertEqual(a1, a2)
    
    # __deepcopy__
    
    def test___deepcopy__(self):
        a1 = NestedDict({"k": {"foo": "bar"}})
        a2 = copy.deepcopy(a1)
        self.assertIsNot(a1, a2)
        self.assertEqual(a1, a2)
        a1.data["k"]["foo"] = "baz"
        self.assertNotEqual(a1, a2)
    
    # __items__
    
    def test___items__(self):
        a = NestedDict({"k": {"foo": "bar"}})
        for item in a.items():
            self.assertIsInstance(item, tuple)
    
    # __keys__
    
    def test___keys__(self):
        a = NestedDict({"k": {"foo": "bar"}})
        for k in a.keys():
            self.assertEqual(k, "k")
    
    # __values__
    
    def test___values__(self):
        a = NestedDict({"k": {"foo": "bar"}})
        for v in a.values():
            self.assertEqual(v, {"foo": "bar"})
    
    # ref
    
    def test_ref__no_args__returns_all_values(self):
        a = NestedDict({"k": {"foo": "bar"}})
        self.assertEqual(a.ref(), {"k": {"foo": "bar"}})
    
    def test_ref__string_arg__returns_value(self):
        a = NestedDict({"k": {"foo": "bar"}})
        self.assertEqual(a.ref("k"), {"foo": "bar"})
    
    def test_ref__string_arg__raises_KeyError(self):
        a = NestedDict()
        with self.assertRaises(KeyError):
            a.ref("k")
    
    def test_ref__string_arg__raises_TypeError(self):
        a = NestedDict({"k": {"foo": "bar"}})
        with self.assertRaises(TypeError):
            a.ref(("k", "foo", "baz"))
    
    def test_ref__path_arg__returns_value(self):
        a = NestedDict({"k1": {"k2": {"k3": "v"}}})
        self.assertEqual(a.ref(("k1", "k2")), ({"k3": "v"}))
    
    def test_ref__create_True__creates_missing_containers(self):
        a = NestedDict()
        a.ref("k", create=True)
        self.assertEqual(a, {"k": {}})
    
    # get
    
    def test_get__string_arg__returns_value(self):
        a = NestedDict({"k": "v"})
        self.assertEqual(a.get("k"), "v")
    
    def test_get__string_arg_missing_key__returns_default_value(self):
        a = NestedDict()
        self.assertEqual(a.get("k", "foo"), "foo")
    
    def test_get__string_arg__raises_KeyError(self):
        a = NestedDict()
        with self.assertRaises(KeyError):
            a.get("k")
    
    def test_get__string_arg__raises_ValueError(self):
        a = NestedDict({"k1": {"k2": "v"}})
        with self.assertRaises(TypeError):
            a.get(("k1", "k2", "k3"))
    
    def test_get__path_arg__returns_value(self):
        a = NestedDict({"k1": {"k2": {"k3": "v"}}})
        self.assertEqual(a.get(("k1", "k2")), {"k3": "v"})
    
    # has
    
    def test_has__returns_True(self):
        a = NestedDict({"k": "v"})
        self.assertTrue(a.has())
    
    def test_has__returns_False(self):
        a = NestedDict()
        self.assertFalse(a.has())
    
    def test_has__tuple_arg__returns_True(self):
        a = NestedDict({"k1": {"k2": {"k3": "v"}}})
        self.assertTrue(a.has(("k1",)))
    
    def test_has__tuple_arg__returns_False(self):
        a = NestedDict({("k1", "k2", "k3"): "v"})
        self.assertFalse(a.has(("foo",)))
    
    def test_has__path_arg__returns_True(self):
        a = NestedDict({"k1": {"k2": {"k3": "v"}}})
        self.assertTrue(a.has(("k1", "k2", "k3")))
    
    def test_has__path_arg__returns_False(self):
        a = NestedDict({"k1": {"k2": {"k3": "v"}}})
        self.assertFalse(a.has(("k1", "k2", "foo")))
    
    # copy
    
    def test_copy(self):
        a1 = NestedDict({"k1": {"k2": {"k3": "v"}}})
        a2 = a1.copy()
        self.assertEqual(a1, a2)
        a1["k1"] = "foo"
        self.assertNotEqual(a1, a2)
    
    # clone
    
    def test_clone(self):
        a1 = NestedDict({"k1": {"k2": {"k3": "v"}}})
        a2 = a1.clone()
        self.assertEqual(a1, a2)
        a1["k1"] = "foo"
        self.assertEqual(a1, a2)
    
    # set
    
    def test_set__string_arg(self):
        a = NestedDict()
        a.set("k", "v")
        self.assertEqual(a, {"k": "v"})
    
    def test_set__delimited_string_key_param(self):
        a = NestedDict()
        a.set(("k1", "k2", "k3"), "v")
        self.assertEqual(a, {"k1": {"k2": {"k3": "v"}}})
    
    def test_set__raises_TypeError(self):
        a = NestedDict({"k1": {"k2": "v"}})
        with self.assertRaises(TypeError):
            a.set(("k1", "k2", "k3"), "v", create=False)
    
    # push
    
    def test_push__string_arg(self):
        a = NestedDict({"k": []})
        a.push("k", "v")
        self.assertEqual(a, {"k": ["v"]})
    
    def test_push__string_arg__convert_existing_value(self):
        a = NestedDict({"k": "v"})
        a.push("k", "v")
        self.assertEqual(a, {"k": ["v", "v"]})
    
    def test_push__path_arg(self):
        a = NestedDict({"k1": {"k2": {"k3": []}}})
        a.push(("k1", "k2", "k3"), "v")
        self.assertEqual(a, {"k1": {"k2": {"k3": ["v"]}}})
    
    def test_push__create_True__creates_list(self):
        a = NestedDict()
        a.push("k", "v")
        self.assertEqual(a, {"k": ["v"]})
    
    def test_push__create_False__raises_KeyError(self):
        a = NestedDict()
        with self.assertRaises(KeyError):
            a.push("k", "v", create=False)
    
    def test_push__create_False__raises_TypeError(self):
        a = NestedDict({"k": "v"})
        with self.assertRaises(AttributeError):
            a.push("k", "v", create=False)
    
    # pull
    
    def test_pull__string_arg(self):
        a = NestedDict({"k": ["v"]})
        a.pull("k", "v")
        self.assertEqual(a, {"k": []})
    
    def test_pull__cleanup_True__removes_empty_containers(self):
        a = NestedDict({"k": ["v"]})
        a.pull("k", "v", cleanup=True)
        self.assertEqual(a, {})
    
    def test_pull__path_arg(self):
        a = NestedDict({"k1": {"k2": {"k3": ["v"]}}})
        a.pull(("k1", "k2", "k3"), "v")
        self.assertEqual(a, {"k1": {"k2": {"k3": []}}})
    
    def test_pull__string_arg__raises_KeyError(self):
        a = NestedDict()
        with self.assertRaises(KeyError):
            a.pull("k", "v")
    
    def test_pull__string_arg__raises_ValueError(self):
        a = NestedDict({"k": []})
        with self.assertRaises(ValueError):
            a.pull("k", "v")
    
    def test_pull__string_arg__raises_TypeError(self):
        a = NestedDict({"k": "v"})
        with self.assertRaises(AttributeError):
            a.pull("k", "v")
    
    # unset
    
    def test_unset__string_arg(self):
        a = NestedDict({"k": "v"})
        a.unset("k")
        self.assertEqual(a, {})
    
    def test_unset__cleanup_True__removes_empty_containers(self):
        a = NestedDict({"k1": {"k2": {"k3": "v"}}})
        a.unset(("k1", "k2", "k3"), cleanup=True)
        self.assertEqual(a, {"k1": {}})
    
    def test_unset__string_arg__raises_KeyError(self):
        a = NestedDict({"k": "v"})
        with self.assertRaises(KeyError):
            a.unset("foo")
    
    # merge
    
    def test_merge__dict_arg(self):
        a = NestedDict({"k1": "v"})
        b = a.merge({"k2": "v"})
        self.assertEqual(b, {"k1": "v", "k2": "v"})
    
    def test_merge__nested_data__nested_data_arg(self):
        a = NestedDict({"k1": {"k2": "v"}})
        b = a.merge({"k1": {"k3": "v"}})
        self.assertEqual(b, {"k1": {"k2": "v", "k3": "v"}})
    
    def test_merge__NestedDict_arg(self):
        a = NestedDict({"k1": "v"})
        b = a.merge(NestedDict({"k2": "v"}))
        self.assertEqual(b, {"k1": "v", "k2": "v"})
    
    def test_merge__incompatible_types(self):
        a = NestedDict({"k1": "v"})
        b = a.merge("foo")
        self.assertEqual(b, {"k1": "v"})
    
    # update
    
    def test_update__dict_arg(self):
        a = NestedDict({"k1": "v"})
        a.update({"k2": "v"})
        self.assertEqual(a, {
            "k1": "v",
            "k2": "v"
        })
    
    def test_update__NestedDict_arg(self):
        a = NestedDict({"k1": "v"})
        a.update(NestedDict({"k2": "v"}))
        self.assertEqual(a, {
            "k1": "v",
            "k2": "v"
        })
    
    # collapse
    
    def test_collapse(self):
        a = NestedDict({"k1": {"k2": {"k3": "v"}}})        
        b = a.collapse()
        self.assertEqual(b, {("k1", "k2", "k3"): "v"})
    
    def test_collapse__function_arg(self):
        a = NestedDict({"k1": {"k2": {"$foo": {"k3": {"k4": "v"}}}}})
    
        def detect_operator(key, *args):
            return key[0] == "$"
    
        b = a.collapse(func=detect_operator)
        self.assertEqual(b, {("k1", "k2"): {"$foo": {("k3", "k4"): "v"}}})


if __name__ == "__main__":
    unittest.main()
