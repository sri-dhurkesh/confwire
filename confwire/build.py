"""Build Python objects from ``"type"``-tagged configuration dictionaries."""

from importlib import import_module
from typing import Any

#: Dotted ``"type"`` paths that are never allowed to be built, regardless
#: of caller-supplied ``blocked_types``, since they allow arbitrary
#: code/command execution.
DEFAULT_BLOCKED_TYPES = frozenset(
    {
        "os.system",
        "os.popen",
        "os.execv",
        "os.execve",
        "os.execvp",
        "os.execvpe",
        "os.spawnl",
        "os.spawnv",
        "os.remove",
        "os.unlink",
        "os.rmdir",
        "shutil.rmtree",
        "subprocess.Popen",
        "subprocess.call",
        "subprocess.run",
        "subprocess.check_call",
        "subprocess.check_output",
        "builtins.eval",
        "builtins.exec",
        "eval",
        "exec",
    }
)


def build_from_config(config_dict: dict, base_package: str | None = None, blocked_types=None):
    """Recursively build an object from a configuration dictionary.

    ``config_dict`` must contain a ``"type"`` key holding a dotted import
    path to the callable to build, either absolute (e.g.
    ``"pkg.module.Class"``) or relative (e.g. ``".module.Class"``, resolved
    against ``base_package``). All other keys are passed as keyword
    arguments to that callable. Any value that is itself a dict is walked
    via :func:`build_value` so nested objects (at any depth) are built
    before being passed to their parent.

    Args:
        config_dict (dict): The configuration to build from. If it has no
          ``"type"`` key, it is returned unchanged (treated as a plain
          data dict rather than an object description).
        base_package (str, optional): Base package to resolve a relative
          ``"type"`` path against. Required only when ``"type"`` starts
          with a dot. Default: None.
        blocked_types (set, optional): Dotted type paths that must never
          be built (e.g. ``"os.system"``). Defaults to
          :data:`DEFAULT_BLOCKED_TYPES` when not provided.

    Returns:
        Any: The instance constructed from ``config_dict``, or
        ``config_dict`` itself (copied) when it has no ``"type"`` key.

    Raises:
        PermissionError: If ``"type"`` matches an entry in the blocklist.
        ImportError: If ``"type"`` is a relative path and no
          ``base_package`` was supplied.
        ModuleNotFoundError: If the module in ``"type"`` cannot be found.
        AttributeError: If the module exists but the class/attribute does
          not.

    Examples:
        >>> build_from_config(
        ...     {"type": "botocore.config.Config", "region_name": "us-east-1"}
        ... )
        <botocore.config.Config object at ...>
    """
    data = config_dict.copy()
    if "type" not in data:
        return data
    import_path = data["type"]

    blocklist = DEFAULT_BLOCKED_TYPES if blocked_types is None else blocked_types
    if import_path in blocklist:
        raise PermissionError(f"Building objects of type '{import_path}' is not allowed.")

    module = ".".join(import_path.split(".")[:-1])
    name_of_object = import_path.split(".")[-1]
    del data["type"]

    if import_path.startswith("."):
        if not base_package:
            raise ImportError(
                f"Cannot resolve relative type '{import_path}' without a "
                "base_package to resolve it against. Pass base_package= "
                "to build_from_config()."
            )
        resolved_module = import_module(module, package=base_package)
    else:
        resolved_module = import_module(module)

    instance = getattr(resolved_module, name_of_object)
    kwargs = {key: build_value(value, base_package, blocked_types) for key, value in data.items()}
    return instance(**kwargs)


def build_value(value: Any, base_package: str | None = None, blocked_types: set | None = None):
    """
    Recursively build any dict value found while building a config.

    Used by :func:`build_from_config` to walk keyword-argument values: a
    dict containing ``"type"`` is built via :func:`build_from_config`, a
    plain dict without ``"type"`` is walked key by key looking for
    buildable objects nested inside it, and any other value (str, int,
    list, etc.) is returned unchanged.

    Args:
        value (Any): The value to inspect and, if applicable, build.
        base_package (str): Base package used to resolve relative
          ``"type"`` paths, forwarded from :func:`build_from_config`.
        blocked_types (set): Dotted type paths that must never be built,
          forwarded from :func:`build_from_config`.

    Returns:
        Any: The built object if ``value`` (or something nested inside
        it) describes one, otherwise ``value`` unchanged.

    Examples:
        >>> build_value({"type": "botocore.config.Config"}, None, None)
        <botocore.config.Config object at ...>
        >>> build_value({"a": 1}, None, None)
        {'a': 1}
    """
    if isinstance(value, dict):
        if "type" in value:
            return build_from_config(value, base_package=base_package, blocked_types=blocked_types)
        return {key: build_value(val, base_package, blocked_types) for key, val in value.items()}
    return value
