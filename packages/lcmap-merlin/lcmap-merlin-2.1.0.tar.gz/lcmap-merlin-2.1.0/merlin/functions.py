"""functions.py is a module of generalized, reusable functions"""

from collections import Counter
from cytoolz import drop
from cytoolz import first
from cytoolz import get_in
from cytoolz import merge
from cytoolz import partial
from cytoolz import reduce
from cytoolz import second
from datetime import datetime
from functools import singledispatch
import functools
import hashlib
import itertools
import json
import logging
import numpy as np
import re

logger = logging.getLogger(__name__)


def extract(sequence, elements):
    """Given a sequence (possibly with nested sequences), extract
    the element identifed by the elements sequence.

    Args:
        sequence: A sequence of elements which may be other sequences
        elements: Sequence of nested element indicies (in sequence parameter)
            to extract

    Returns:
        The target element

    Example:
        >>> inputs = [1, (2, 3, (4, 5)), 6]
        >>> extract(inputs, [0])
        >>> 1
        >>> extract(inputs, [1])
        >>> (2, 3, (4, 5))
        >>> extract(inputs, [1, 0])
        >>> 2
        >>> extract(inputs, [1, 1])
        >>> 3
        >>> extract(inputs, [1, 2])
        >>> (4, 5)
        >>> extract(inputs, [1, 2, 0])
        >>> 4
    ...
    """

    e = tuple(elements)
    if len(e) == 0 or not getattr(sequence, '__iter__', False):
        return sequence
    else:
        seq = sequence[first(e)]
        return extract(seq, drop(1, e))


def flatten(iterable):
    """Reduce dimensionality of iterable containing iterables

    Args:
        iterable: A multi-dimensional iterable

    Returns:
        A one dimensional iterable
    """

    return itertools.chain.from_iterable(iterable)


def intersection(items):
    """Returns the intersecting set contained in items

    Args:
        items: Two dimensional sequence of items

    Returns:
        Intersecting set of items

    Example:
        >>> items = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
        >>> intersection(items)
        {3}
    """

    return set.intersection(*(map(lambda x: set(x), items)))


@functools.lru_cache(maxsize=128, typed=True)
def minbox(points):
    """Returns the minimal bounding box necessary to contain points

    Args:
        points (tuple): (x,y) points: ((0,0), (40, 55), (66, 22))

    Returns:
        dict: ulx, uly, lrx, lry
    """

    x, y = [point[0] for point in points], [point[1] for point in points]
    return {'ulx': min(x), 'lrx': max(x), 'lry': min(y), 'uly': max(y)}


def sha256(string):
    """Computes and returns a sha256 digest of the supplied string

    Args:
        string (str): string to digest

    Returns:
        digest value
    """

    return hashlib.sha256(string.encode('UTF-8')).hexdigest()


def md5(string):
    """Computes and returns an md5 digest of the supplied string

    Args:
        string: string to digest

    Returns:
        digest value
    """

    return hashlib.md5(string.encode('UTF-8')).hexdigest()


def sort(iterable, key=None):
    """Sorts an iterable"""

    return sorted(iterable, key=key, reverse=False)


def rsort(iterable, key=None):
    """Reverse sorts an iterable"""

    return sorted(iterable, key=key, reverse=True)


@singledispatch
def serialize(arg):
    """Converts datastructure to json, computes digest

    Args:
        dictionary: A python dict

    Returns:
        tuple: (digest,json)
    """

    s = json.dumps(arg, sort_keys=True, separators=(',', ':'),
                   ensure_ascii=True)
    return md5(s), s


@serialize.register(set)
def _(arg):
    """Converts set to list then serializes the resulting value"""

    return serialize(sorted(list(arg)))


def deserialize(string):
    """Reconstitues datastructure from a string.

    Args:
        string: A serialized data structure

    Returns:
        Data structure represented by string parameter
    """

    return json.loads(string)


def flip_keys(dods):
    """Accepts a dictionary of dictionaries and flips the outer and inner keys.
    All inner dictionaries must have a consistent set of keys or key Exception
    is raised.

    Args:
        dods: dict of dicts

    Returns:
        dict of dicts with inner and outer keys flipped

    Example:
        >>> dods = {"reds":   {(0, 0): [110, 110, 234, 664],
                               (0, 1): [23, 887, 110, 111]},
                    "greens": {(0, 0): [120, 112, 224, 624],
                               (0, 1): [33, 387, 310, 511]},
                    "blues":  {(0, 0): [128, 412, 244, 654],
                               (0, 1): [73, 987, 119, 191]},
        >>> flip_keys(dods)
        {(0, 0): {"reds":   [110, 110, 234, 664],
                  "greens": [120, 112, 224, 624],
                  "blues":  [128, 412, 244, 654], ... },
         (0, 1), {"reds":   [23, 887, 110, 111],
                  "greens": [33, 387, 310, 511],
                  "blues":  [73, 987, 119, 191], ... }}

    """

    def flip(innerkeys, outerkeys, inputs):
        for ik in innerkeys:
            yield({ik: {ok: inputs[ok][ik] for ok in outerkeys}})

    outerkeys = set(dods.keys())
    innerkeys = set(reduce(lambda accum, v: accum + v,
                           [list(dods[ok].keys()) for ok in outerkeys]))
    return merge(flip(innerkeys, outerkeys, dods))


def cqlstr(string):
    """Makes a string safe to use in Cassandra CQL commands

    Args:
        string: The string to use in CQL

    Returns:
        str: A safe string replacement
    """

    return re.sub('[-:.]', '_', string)


def represent(item):
    """Represents callables and values consistently

    Args:
        item: The item to represent

    Returns:
        Item representation
    """

    return repr(item.__name__) if callable(item) else repr(item)


def isnumeric(value):
    """Does a string value represent a number (positive or negative?)

    Args:
        value (str): A string

    Returns:
        bool: True or False
    """

    try:
        float(value)
        return True
    except:
        return False


def timed(f):
    """Timing wrapper for functions.  Prints start and stop time to INFO
    along with function name, arguments and keyword arguments.

    Args:
        f (function): Function to be timed

    Returns:
        function: Wrapped function
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        """Wrapper function."""
        msg = '{}(args={}, kwargs={}):'.format(f.__name__,  args, kwargs)
        logger.info('{} start:{}'.format(msg, datetime.now().isoformat()))
        r = f(*args, **kwargs)
        logger.info('{} stop:{}'.format(msg, datetime.now().isoformat()))
        return r
    return wrapper


def seqeq(a, b):
    """Determine if two unordered sequences are equal.

    Args:
        a: sequence a
        b: sequence b

    Returns:
        bool: True or False
    """

    #runs in linear (On) time.
    return Counter(a) == Counter(b)


def issubset(a, b):
    """Determines if a exists in b

    Args:
        a: sequence a
        b: sequence b

    Returns:
        bool: True or False
    """

    return set(a).issubset(set(b))


def difference(a, b):
    """Subtracts items in b from items in a.

    Args:
        a: sequence a
        b: sequence b

    Returns:
        set: items that exist in a but not b
    """

    return set(a) - set(b)


def chexists(dictionary, keys, check_fn):
    """applies check_fn against dictionary minus keys then ensures the items
    returned from check_fn exist in dictionary[keys]

    Args:
        dictionary (dict): {key: [v1, v3, v2]}
        keys (sequence): A sequence of keys in dictionary
        check_fn (function): Function that accepts dict and returns
                             sequence of items or Exception

    Returns:
        A sequence of items that are returned from check_fn and exist in
        dictionary[keys] or Exception
    """

    def exists_in(superset, subset):
        if issubset(subset, second(superset)):
            return True
        else:
            msg =  '{} is missing data.'.format(first(superset))
            msg2 = '{} is not a subset of {}'.format(subset, second(superset))
            raise Exception('\n\n'.join([msg, msg2]))

    popped  = {k: dictionary[k] for k in keys}
    checked = check_fn({k: dictionary[k] for k in difference(dictionary, keys)})
    all(map(partial(exists_in, subset=checked), popped.items()))
    return checked


def insert_into_every(dods, key, value):
    """Insert key:values into every subdictionary of dods.

    Args:
        dods: dictionary of dictionaries
        key: key to hold values in subdictionaires
        value: value to associate with key

    Returns:
        dict: dictionary of dictionaries with key:values inserted into each
    """

    def update(d, v):
        d.update({key: v})
        return d

    return {k: update(v, value) for k, v in dods.items()}


def coordinates(ulx, uly, lrx, lry, grid, cfg):
    """Returns all the coordinates that are needed to cover a supplied
    bounding box.

    Args:
        ulx  (float)   : upper left x
        uly  (float)   : upper left y
        lrx  (float)   : lower right x
        lry  (float)   : lower right y
        grid (dict)    : {'name': 'chip', 'sx': 3000, 'sy': 3000, 'rx': 1, 'ry': -1}
        cfg  (dict)    : A Merlin configuration

    Returns:
        tuple: tuple of tuples of chip coordinates ((x1,y1), (x2,y1) ...)

    This example assumes chip sizes of 500 pixels.

    Example:
        >>> coordinates = coordinates(ulx=-1000, 
                                      uly=1000, 
                                      lrx=-500, 
                                      lry=500,
                                      grid={'name': 'chip', 'sx': 500, 'sy': 500, 'rx': 1, 'ry': -1}, 
                                      cfg={'snap_fn': some_func})

        ((-1000, 500), (-500, 500), (-1000, -500), (-500, -500))
    """
    
    # get the snap_fn from Merlin config
    snap_fn = cfg.get('snap_fn')

    # snap start/end x & y
    start_x, start_y = get_in([grid.get('name'), 'proj-pt'], snap_fn(x=ulx, y=uly))
    end_x,   end_y   = get_in([grid.get('name'), 'proj-pt'], snap_fn(x=lrx, y=lry))

    # get x and y scale factors multiplied by reflection
    x_interval = grid.get('sx') * grid.get('rx')
    y_interval = grid.get('sy') * grid.get('ry')
    
    return tuple((x, y) for x in np.arange(start_x, end_x + x_interval, x_interval)
                        for y in np.arange(start_y, end_y + y_interval, y_interval))


def bounds_to_coordinates(bounds, grid, cfg):
    """Returns coordinates from a sequence of bounds.  Performs minbox
    operation on bounds, thus irregular geometries may be supplied.

    Args:
        bounds: a sequence of bounds.
        grid (dict): {'name': 'chip', 'sx': SCALE_FACTOR, 'sy': SCALE_FACTOR, 'rx': 1, 'ry': -1}
        cfg (dict): {'snap_fn': some_func}

    Returns:
        tuple: chip coordinates

    Example:
        >>> xys = bounds_to_coordinates(
                                    bounds=((112, 443), (112, 500), (100, 443)),
                                    grid={'sx': 3000, 'sy': 3000}, 
                                    cfg={'snap_fn': some_func})
        >>> ((100, 500),)
    """

    return coordinates(ulx=minbox(bounds)['ulx'],
                       uly=minbox(bounds)['uly'],
                       lrx=minbox(bounds)['lrx'],
                       lry=minbox(bounds)['lry'],
                       grid=grid,
                       cfg=cfg)
