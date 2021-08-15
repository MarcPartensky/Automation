#!/usr/bin/env python

"""Absraction over pyyaml.
Use yaml file as a python object."""

import functools
import yaml


class Storage:
    """Abstraction over pyyaml."""

    def __init__(self, file: str):
        """Interface for using pyyaml as a python object."""
        self._file = file

    @property
    def _node(self):
        """Return node."""
        return DictNode(self)

    @property
    def _dict(self):
        """Return node."""
        with open(self._file, "r") as stream:
            content = yaml.safe_load(stream) or {}
        return content

    def __getattribute__(self, key: str):
        """Get an attribute from the yaml object."""
        if key.startswith("_"):
            return super().__getattribute__(key)
        return self._get([key])

    def __setattr__(self, key: str, value):
        """Set a key/value pair."""
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            self._set([], key, value)

    def _get(self, key_path: list, raw=False):
        """Get a value given a key path."""
        with open(self._file, "r") as stream:
            content = yaml.safe_load(stream) or {}
        value = functools.reduce(lambda a, b: a[b], [content] + key_path)
        if not raw and isinstance(value, dict):
            return DictNode(self, key_path)
        elif not raw and isinstance(value, list):
            return ListNode(self, key_path)
        return value

    def _set(self, key_path: list, key, value):
        """Set a value given a key path."""
        with open(self._file, "r") as stream:
            content = yaml.safe_load(stream) or {}
        node = functools.reduce(lambda node, key: node[key], [content] + key_path)
        node[key] = value
        with open(self._file, "w") as stream:
            yaml.safe_dump(content, stream)

    def _append(self, key_path: list, value):
        """Append an element to a list inside the storage document."""
        with open(self._file, "r") as stream:
            content = yaml.safe_load(stream) or {}
        node = functools.reduce(lambda node, key: node[key], [content] + key_path)
        node.append(value)
        with open(self._file, "w") as stream:
            yaml.safe_dump(content, stream)

    def __str__(self):
        """Return string representation of a node."""
        return f"Storage({self._dict})"

    @property
    def raw(self):
        """Return the true python representation."""
        return self([], raw=True)


class Node:
    """Return a node inside the pyyaml document."""

    def __init__(self, storage: Storage, key_path: list = []):
        """Create a given a storage and a key path."""
        self._storage: Storage = storage
        self._key_path: list = key_path

    @property
    def raw(self):
        """Return the true python representation."""
        return self._storage._get(self._key_path, raw=True)

    def __str__(self):
        """Return string representation of a node."""
        content = self._storage._get(self._key_path, raw=True)
        return f"{type(self).__name__}({content})"


class DictNode(Node):
    """Dict node in pyyaml storage."""

    def __getattribute__(self, key):
        """Return the attribute of the node."""
        if key.startswith("_"):
            return super().__getattribute__(key)
        value = self._storage._get(self._key_path + [key])
        if isinstance(value, dict):
            value = DictNode(self, self._key_path + [key])
        return value

    def __setattr__(self, key: str, value):
        """Set a key/value pair."""
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            self._storage._set(self._key_path, key, value)


class ListNode(Node):
    """List node in pyyaml storage."""

    def __getitem__(self, index: int):
        """Return an item from the list node."""
        value = self._storage._get(self._key_path + [index])
        if isinstance(value, dict):
            value = DictNode(self, self._key_path + [index])
        if isinstance(value, list):
            value = ListNode(self, self._key_path + [index])
        return value

    def __setitem__(self, index: int, value):
        """Set a key/value pair."""
        self._storage._set(self._key_path, index, value)

    def __len__(self):
        """Return the length of the list node."""
        return len(self._storage._get(self._key_path).raw)

    def append(self, value):
        """Append an element to the list node."""
        self._storage._append(self._key_path, value)


if __name__ == "__main__":
    from rich import print

    storage = Storage("storage.yml")
    print(storage)
    # print(storage.a)
    storage.a = 1
    storage.b = dict(c=2, d=3)
    storage.c = [1, 2, 3]
    storage.c.append(4)
    b = storage.b
    print("b:", b)
    print("b.c", b.c)
    print(storage.b.c)
    storage.salut = "hola"
