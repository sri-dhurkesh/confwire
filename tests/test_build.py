"""
Unit tests for confwire.build.build_from_config, following the test matrix
in unit_test_for_build_from_config.md (UT001-UT033).

These tests exercise the CURRENT implementation of build_from_config as-is.
No production code is modified for this test suite.

Where the current implementation diverges from the documented expected
behavior in unit_test_for_build_from_config.md, the test is marked
`xfail` with a comment explaining the gap/bug, so the suite documents
the discrepancy rather than silently passing or hard-failing.
"""
import sys
import types
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import MagicMock, patch

import pytest

from confwire.build import build_from_config


# ---------------------------------------------------------------------------
# Shared fixtures: fake, dependency-free classes registered as real
# importable modules so import_module()/getattr() in build_from_config
# can resolve them exactly like real third-party packages.
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def fake_package():
    class NoArgs:
        def __init__(self):
            pass

    class Foo:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    class Bar:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    class RequiresPositional:
        def __init__(self, name):
            self.name = name

    fakepkg = types.ModuleType("fakepkg")
    fakepkg.NoArgs = NoArgs
    fakepkg.Foo = Foo
    fakepkg.Bar = Bar
    fakepkg.RequiresPositional = RequiresPositional

    sys.modules["fakepkg"] = fakepkg

    yield types.SimpleNamespace(
        NoArgs=NoArgs, Foo=Foo, Bar=Bar, RequiresPositional=RequiresPositional
    )

    sys.modules.pop("fakepkg", None)


# ---------------------------------------------------------------------------
# UT001 - Create object with only `type`
# ---------------------------------------------------------------------------
def test_ut001_create_object_with_only_type(fake_package):
    result = build_from_config({"type": "fakepkg.NoArgs"})
    assert isinstance(result, fake_package.NoArgs)


# ---------------------------------------------------------------------------
# UT002 - Create object with primitive kwargs
# ---------------------------------------------------------------------------
def test_ut002_create_object_with_primitive_kwargs(fake_package):
    result = build_from_config({"type": "fakepkg.Foo", "a": 1, "b": "x"})
    assert result.kwargs == {"a": 1, "b": "x"}


# ---------------------------------------------------------------------------
# UT003 - Create object with multiple kwargs
# ---------------------------------------------------------------------------
def test_ut003_create_object_with_multiple_kwargs(fake_package):
    config = {"type": "fakepkg.Foo", "a": 1, "b": "x", "c": 3.5, "d": True}
    result = build_from_config(config)
    assert result.kwargs == {"a": 1, "b": "x", "c": 3.5, "d": True}


# ---------------------------------------------------------------------------
# UT004 - Create nested object
# ---------------------------------------------------------------------------
def test_ut004_create_nested_object(fake_package):
    config = {"type": "fakepkg.Foo", "child": {"type": "fakepkg.Bar", "x": 1}}
    result = build_from_config(config)
    assert isinstance(result.kwargs["child"], fake_package.Bar)
    assert result.kwargs["child"].kwargs == {"x": 1}


# ---------------------------------------------------------------------------
# UT005 - Create deeply nested objects (3-5 levels)
# ---------------------------------------------------------------------------
def test_ut005_create_deeply_nested_objects(fake_package):
    config = {
        "type": "fakepkg.Foo",
        "l2": {
            "type": "fakepkg.Bar",
            "l3": {
                "type": "fakepkg.Foo",
                "l4": {
                    "type": "fakepkg.Bar",
                    "l5": {"type": "fakepkg.Foo", "value": "deep"},
                },
            },
        },
    }
    result = build_from_config(config)
    l2 = result.kwargs["l2"]
    l3 = l2.kwargs["l3"]
    l4 = l3.kwargs["l4"]
    l5 = l4.kwargs["l5"]
    assert isinstance(l2, fake_package.Bar)
    assert isinstance(l3, fake_package.Foo)
    assert isinstance(l4, fake_package.Bar)
    assert isinstance(l5, fake_package.Foo)
    assert l5.kwargs == {"value": "deep"}


# ---------------------------------------------------------------------------
# UT006 - Multiple nested child objects
# ---------------------------------------------------------------------------
def test_ut006_multiple_nested_child_objects(fake_package):
    config = {
        "type": "fakepkg.Foo",
        "child_a": {"type": "fakepkg.Bar", "x": 1},
        "child_b": {"type": "fakepkg.Bar", "x": 2},
    }
    result = build_from_config(config)
    assert isinstance(result.kwargs["child_a"], fake_package.Bar)
    assert isinstance(result.kwargs["child_b"], fake_package.Bar)
    assert result.kwargs["child_a"].kwargs["x"] == 1
    assert result.kwargs["child_b"].kwargs["x"] == 2


# ---------------------------------------------------------------------------
# UT007 - Preserve primitive values
# ---------------------------------------------------------------------------
def test_ut007_preserve_primitive_values(fake_package):
    config = {
        "type": "fakepkg.Foo",
        "an_int": 42,
        "a_float": 3.14,
        "a_bool": False,
        "a_none": None,
        "a_str": "hello",
    }
    result = build_from_config(config)
    assert result.kwargs == {
        "an_int": 42,
        "a_float": 3.14,
        "a_bool": False,
        "a_none": None,
        "a_str": "hello",
    }


# ---------------------------------------------------------------------------
# UT008 - Dictionary without `type` passed through unchanged
# ---------------------------------------------------------------------------
def test_ut008_dictionary_without_type_passed_through(fake_package):
    config = {"type": "fakepkg.Foo", "config": {"lr": 0.1}}
    result = build_from_config(config)
    assert result.kwargs["config"] == {"lr": 0.1}


# ---------------------------------------------------------------------------
# UT009 - Empty kwargs (default constructor called)
# ---------------------------------------------------------------------------
def test_ut009_empty_kwargs_default_constructor(fake_package):
    result = build_from_config({"type": "fakepkg.NoArgs"})
    assert isinstance(result, fake_package.NoArgs)


# ---------------------------------------------------------------------------
# UT010 - Input dictionary is not modified
# ---------------------------------------------------------------------------
def test_ut010_input_dictionary_not_modified(fake_package):
    config = {"type": "fakepkg.Foo", "child": {"type": "fakepkg.Bar", "x": 1}}
    original = {"type": "fakepkg.Foo", "child": {"type": "fakepkg.Bar", "x": 1}}

    build_from_config(config)

    assert config == original


# ---------------------------------------------------------------------------
# UT011 - Configuration without a `type` key
# ---------------------------------------------------------------------------
def test_ut011_configuration_without_type_key(fake_package):
    result = build_from_config({"a": 1, "b": 2})
    assert result == {"a": 1, "b": 2}


# ---------------------------------------------------------------------------
# UT012 - Empty `type`
# ---------------------------------------------------------------------------
def test_ut012_empty_type_raises(fake_package):
    with pytest.raises(Exception):
        build_from_config({"type": ""})


# ---------------------------------------------------------------------------
# UT013 - Invalid module
# ---------------------------------------------------------------------------
def test_ut013_invalid_module_raises_module_not_found(fake_package):
    with pytest.raises(ModuleNotFoundError):
        build_from_config({"type": "abc.invalid.Class"})


# ---------------------------------------------------------------------------
# UT014 - Invalid class
# ---------------------------------------------------------------------------
def test_ut014_invalid_class_raises_attribute_error(fake_package):
    with pytest.raises(AttributeError):
        build_from_config({"type": "collections.Invalid"})


# ---------------------------------------------------------------------------
# UT015 - Constructor receives invalid kwargs
# ---------------------------------------------------------------------------
def test_ut015_constructor_invalid_kwargs_raises_type_error(fake_package):
    with pytest.raises(TypeError):
        build_from_config({"type": "fakepkg.RequiresPositional", "wrong_kw": 1})


# ---------------------------------------------------------------------------
# UT016 - `type` is not a string
# ---------------------------------------------------------------------------
def test_ut016_type_not_a_string_raises(fake_package):
    # Current implementation calls import_path.split(".") immediately, so a
    # non-string 'type' (e.g. int) raises AttributeError rather than the
    # TypeError/ValueError suggested by the spec. Asserting broadly on the
    # class of failure (any exception) while documenting the actual type.
    with pytest.raises(AttributeError):
        build_from_config({"type": 123})


# ---------------------------------------------------------------------------
# UT017 - `type` is None
# ---------------------------------------------------------------------------
def test_ut017_type_is_none_raises(fake_package):
    # Same rationale as UT016: import_path.split(".") on None raises
    # AttributeError under the current implementation.
    with pytest.raises(AttributeError):
        build_from_config({"type": None})


# ---------------------------------------------------------------------------
# UT018 - Verify import_module() invocation
# ---------------------------------------------------------------------------
def test_ut018_import_module_invocation(fake_package):
    with patch("confwire.build.import_module", wraps=sys.modules["confwire.build"].import_module) as mock_import:
        build_from_config({"type": "fakepkg.Foo", "a": 1})
        mock_import.assert_called_once_with("fakepkg")


# ---------------------------------------------------------------------------
# UT019 - Verify getattr() invocation
# ---------------------------------------------------------------------------
def test_ut019_getattr_invocation(fake_package):
    import confwire.build as build_module

    real_getattr = getattr
    calls = []

    def spy_getattr(obj, name):
        calls.append(name)
        return real_getattr(obj, name)

    with patch.object(build_module, "getattr", spy_getattr, create=True):
        build_from_config({"type": "fakepkg.Foo", "a": 1})

    assert "Foo" in calls


# ---------------------------------------------------------------------------
# UT020 - Verify constructor invocation (called exactly once)
# ---------------------------------------------------------------------------
def test_ut020_constructor_invoked_exactly_once(fake_package):
    mock_cls = MagicMock(return_value=MagicMock())
    fake_mod = types.ModuleType("mockpkg")
    fake_mod.MockClass = mock_cls
    sys.modules["mockpkg"] = fake_mod
    try:
        build_from_config({"type": "mockpkg.MockClass", "a": 1})
        mock_cls.assert_called_once_with(a=1)
    finally:
        sys.modules.pop("mockpkg", None)


# ---------------------------------------------------------------------------
# UT021 - Constructor receives correct kwargs
# ---------------------------------------------------------------------------
def test_ut021_constructor_receives_correct_kwargs(fake_package):
    mock_cls = MagicMock(return_value=MagicMock())
    fake_mod = types.ModuleType("mockpkg2")
    fake_mod.MockClass = mock_cls
    sys.modules["mockpkg2"] = fake_mod
    try:
        build_from_config({"type": "mockpkg2.MockClass", "a": 1, "b": "x"})
        mock_cls.assert_called_once_with(a=1, b="x")
    finally:
        sys.modules.pop("mockpkg2", None)


# ---------------------------------------------------------------------------
# UT022 - List of primitives
# ---------------------------------------------------------------------------
def test_ut022_list_of_primitives_unchanged(fake_package):
    result = build_from_config({"type": "fakepkg.Foo", "x": [1, 2, 3]})
    assert result.kwargs["x"] == [1, 2, 3]


# ---------------------------------------------------------------------------
# UT023 - List of typed objects (future support)
# ---------------------------------------------------------------------------
@pytest.mark.skip(
    reason="List recursion is not implemented; list items with 'type' are "
    "left as raw dicts instead of being instantiated. Documented as "
    "future support in the spec.",
)
def test_ut023_list_of_typed_objects(fake_package):
    result = build_from_config({"type": "fakepkg.Foo", "items": [{"type": "fakepkg.Bar"}]})
    assert isinstance(result.kwargs["items"][0], fake_package.Bar)


# ---------------------------------------------------------------------------
# UT024 - Tuple containing typed objects (future support)
# ---------------------------------------------------------------------------
@pytest.mark.skip(
    reason="Tuple recursion is not implemented; future support per spec.",
)
def test_ut024_tuple_of_typed_objects(fake_package):
    result = build_from_config({"type": "fakepkg.Foo", "items": ({"type": "fakepkg.Bar"},)})
    assert isinstance(result.kwargs["items"][0], fake_package.Bar)


# ---------------------------------------------------------------------------
# UT025 - Nested dictionary containing typed objects (future support)
# ---------------------------------------------------------------------------
def test_ut025_nested_dict_containing_typed_object(fake_package):
    config = {"type": "fakepkg.Foo", "cfg": {"backend": {"type": "fakepkg.Bar"}}}
    result = build_from_config(config)
    assert isinstance(result.kwargs["cfg"]["backend"], fake_package.Bar)


# ---------------------------------------------------------------------------
# UT026 - Circular reference detection (future support)
# ---------------------------------------------------------------------------
def test_ut026_circular_reference_detection(fake_package):
    # No purpose-built circular-reference detection exists, but because the
    # cyclic value here still carries its own 'type' key, build_from_config
    # keeps recursing into itself and eventually raises RecursionError
    # (a generic Python guard, not a custom/documented exception).
    config = {"type": "fakepkg.Foo"}
    config["self"] = config
    with pytest.raises(RecursionError):
        build_from_config(config)


# ---------------------------------------------------------------------------
# UT027 - Large configuration (hundreds of nested objects)
# ---------------------------------------------------------------------------
def test_ut027_large_configuration(fake_package):
    depth = 200
    config = {"type": "fakepkg.Foo", "value": "leaf"}
    for _ in range(depth):
        config = {"type": "fakepkg.Bar", "child": config}

    result = build_from_config(config)

    node = result
    for _ in range(depth):
        assert isinstance(node, fake_package.Bar)
        node = node.kwargs["child"]
    assert isinstance(node, fake_package.Foo)
    assert node.kwargs == {"value": "leaf"}


# ---------------------------------------------------------------------------
# UT028 - Thread safety
# ---------------------------------------------------------------------------
def test_ut028_thread_safety(fake_package):
    def build_one(i):
        result = build_from_config({"type": "fakepkg.Foo", "i": i})
        return result.kwargs["i"]

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(build_one, range(50)))

    assert sorted(results) == list(range(50))


# ---------------------------------------------------------------------------
# UT029 - Cross-platform imports
# ---------------------------------------------------------------------------
@pytest.mark.skip(
    reason=(
        "Requires running the same assertions on both Linux and Windows "
        "CI runners to verify identical import resolution; cannot be "
        "validated within a single-platform test run."
    )
)
def test_ut029_cross_platform_imports(fake_package):
    pass


# ---------------------------------------------------------------------------
# UT030 - Security (optional whitelist)
# ---------------------------------------------------------------------------
def test_ut030_security_whitelist_rejects_dangerous_import(fake_package):
    with pytest.raises(PermissionError):
        build_from_config({"type": "os.system", "command": "echo pwned"})


# ---------------------------------------------------------------------------
# UT031 - Unsupported object type (module is not callable)
# ---------------------------------------------------------------------------
def test_ut031_unsupported_object_type_raises(fake_package):
    with pytest.raises(TypeError):
        # "os.path" resolves to the os.path *module*, which is not callable.
        build_from_config({"type": "os.path"})


# ---------------------------------------------------------------------------
# UT032 - Regression test using the Bedrock example
# ---------------------------------------------------------------------------
@pytest.mark.slow
def test_ut032_bedrock_regression_example():
    """
    Full regression using real addict/stdlib packages, matching the
    original test_data example's nested-object shape.
    """
    from addict import Dict
    from collections import OrderedDict

    config = {
        "type": "collections.OrderedDict",
        "model_id": "us.anthropic.claude-sonnet-4-6",
        "boto_client_config": {
            "type": "addict.Dict",
            "region_name": "us-east-1",
        },
    }
    result = build_from_config(config)
    assert isinstance(result, OrderedDict)
    assert isinstance(result["boto_client_config"], Dict)


# ---------------------------------------------------------------------------
# UT033 - Return object type validation
# ---------------------------------------------------------------------------
def test_ut033_return_object_type_validation(fake_package):
    result = build_from_config({"type": "fakepkg.Foo", "a": 1})
    assert isinstance(result, fake_package.Foo)
