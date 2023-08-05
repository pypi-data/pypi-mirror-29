import bisect
from collections import abc

import numpy as np

from gameanalysis import utils


def mcces(thresh):
    return MinimumConnectedComponentElementSet(thresh)


class MinimumConnectedComponentElementSet(object):
    """A class for returning vectors with the minimum weight

    Vectors are only returned if they have the minimum weight in their
    connected component, where two vectors are connected if they're closer than
    `thresh` distance apart.

    Inserts can take up to `O(n)` where `n` is the number of elements inserted.
    If this is problematic, a better data structure will probably be
    necessary."""

    def __init__(self, thresh):
        self._thresh = thresh ** 2
        self._set = []

    def _similar(self, a, b):
        return sum((ai - bi) ** 2 for ai, bi in zip(a, b)) <= self._thresh

    def add(self, vector, weight):
        """Add a vector with a weight

        Returns true if the element is distinct from every element in the
        container"""
        vector = tuple(vector)
        mins = (weight, vector)
        vecs = [vector]
        new_set = []
        for set_tup in self._set:
            smin, svecs = set_tup
            if any(self._similar(vector, v) for v in svecs):
                mins = min(smin, mins)
                vecs.extend(svecs)
            else:
                new_set.append(set_tup)

        bisect.insort(new_set, (mins, vecs))
        self._set = new_set
        return len(vecs) == 1

    def clear(self):
        self._set.clear()

    def __len__(self):
        return len(self._set)

    def __iter__(self):
        return iter((v, w) for (w, v), _ in self._set)

    def __repr__(self):
        return '{}({}, {})'.format(
            self.__class__.__name__, self._thresh, list(self))


@utils.deprecated
class WeightedSimilaritySet(object):
    """A set of non-similar elements prioritized by weight

    Allows adding a bunch of weighted elements, and when iterated, only
    iterates over dissimilar elements with the lowest weights. Adding new
    elements that are similar to the existing set, but with higher weights
    won't change the set returned."""

    def __init__(self, is_similar):
        self._is_similar = is_similar
        self._i = 0  # Tie breaking
        self._items = []
        self._set = []
        self._computed = True

    def add(self, item, weight):
        self._computed = False
        self._set.clear()
        self._items.append((weight, self._i, item))
        self._i += 1
        return self

    def clear(self):
        self._i = 0
        self._items.clear()
        self._set.clear()
        self._computed = True

    def _satisfy(self):
        if not self._computed:
            self._items.sort()
            for w, _, i in self._items:
                if all(not self._is_similar(i, j) for j, _ in self._set):
                    self._set.append((i, w))
            self._computed = True

    def __len__(self):
        self._satisfy()
        return len(self._set)

    def __iter__(self):
        self._satisfy()
        return iter(self._set)

    def __repr__(self):
        self._satisfy()
        suffix = ('.add(' + ').add('.join('{}, {}'.format(i, w)
                                          for w, _, i in self._items) + ')'
                  if self._items else '')
        return '{}({}){}'.format(self.__class__.__name__,
                                 self._is_similar.__name__, suffix)


class DynamicArray(object):
    """A object with a backed array that also allows adding data"""

    def __init__(self, item_shape, dtype=None, initial_room=8,
                 grow_fraction=2):
        assert grow_fraction > 1
        if not isinstance(item_shape, abc.Sized):
            item_shape = (item_shape,)
        self._data = np.empty((initial_room,) + tuple(item_shape), dtype)
        self._length = 0
        self._grow_fraction = 2

    def append(self, array):
        """Append an array"""
        array = np.asarray(array, self._data.dtype)
        if array.shape[1:] == self._data.shape[1:]:
            # Adding multiple
            num = array.shape[0]
            self.ensure_capacity(self._length + num)
            self._data[self._length:self._length + num] = array
            self._length += num

        elif array.shape == self._data.shape[1:]:
            # Adding one
            self.ensure_capacity(self._length + 1)
            self._data[self._length] = array
            self._length += 1

        else:
            raise ValueError("Invalid shape for append")

    def pop(self, num=None):
        """Pop one or several arrays"""
        if num is None:
            assert self._length > 0, "can't pop from an empty array"
            self._length -= 1
            return self._data[self._length].copy()

        else:
            assert num >= 0 and self._length >= num
            self._length -= num
            return self._data[self._length:self._length + num].copy()

    @property
    def data(self):
        """A view of all of the data"""
        return self._data[:self._length]

    def ensure_capacity(self, new_capacity):
        """Make sure the array has a least new_capacity"""
        if new_capacity > self._data.shape[0]:
            growth = round(self._data.shape[0] * self._grow_fraction) + 1
            new_size = max(growth, new_capacity)
            new_data = np.empty((new_size,) + self._data.shape[1:],
                                self._data.dtype)
            new_data[:self._length] = self._data[:self._length]
            self._data = new_data

    def compact(self):
        """Trim underlying storage to hold only valid data"""
        self._data = self.data.copy()
        self._length = self._data.shape[0]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return self._length

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return repr(self.data)


def bitset():
    return BitSet()


class BitSet(object):
    """Set of bitmasks

    A bitmask is in the set if all of the true bits have been added
    together. When iterating, all maximal bitsets are returned."""
    # This compresses all bitmasks down to the number they are
    # implicitly, and uses bitwise math to replicate the same functions.

    def __init__(self):
        self._masks = []

    def add(self, bitmask):
        bitmask = np.asarray(bitmask, bool)
        if not self._masks:
            self._mask = 2 ** np.arange(bitmask.size)
        if bitmask not in self:
            num = bitmask.dot(self._mask)
            self._masks[:] = [m for m in self._masks if m & ~num]
            self._masks.append(num)
            return True
        else:
            return False

    def clear(self):
        self._masks.clear()

    def __contains__(self, bitmask):
        if not self._masks:
            return False
        assert bitmask.size == self._mask.size, \
            "can't add bitmasks of different sizes"
        num = bitmask.dot(self._mask)
        return not all(num & ~m for m in self._masks)

    def __iter__(self):
        return ((m // self._mask % 2).astype(bool) for m in self._masks)

    def __bool__(self):
        return bool(self._masks)

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self._masks)


@utils.deprecated
class MixtureSet(object):
    """A set of mixtures

    Elements are only kept if the norm of their difference is greater than the
    tolerance."""

    def __init__(self, tolerance):
        self._tol = tolerance ** 2
        self._mixtures = []

    def add(self, mixture):
        if mixture not in self:
            self._mixtures.append(mixture)
            return True
        else:
            return False

    def clear(self):
        self._mixtures.clear()

    def __contains__(self, mix):
        return any(np.dot(m - mix, m - mix) <= self._tol for m in self)

    def __bool__(self):
        return bool(self._mixtures)

    def __len__(self):
        return len(self._mixtures)

    def __iter__(self):
        return iter(self._mixtures)

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self._mixtures)
