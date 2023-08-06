# encoding: utf-8

import logging_helper
from copy import deepcopy
from collections import Mapping
from future.utils import iteritems
from classutils.decorators import deprecated
from .cfg_item import CfgItem

logging = logging_helper.setup_logging()


class CfgItems(Mapping):

    def __init__(self,
                 cfg_fn,
                 cfg_root,
                 key_name,
                 has_active=False,
                 allowed_items=None,
                 item_class=CfgItem,
                 **overrides):

        """
        
        :param cfg_fn:          Function that retrieves the config object for this item.
        :param cfg_root:        Root config key to use for this config.
        :param key_name:        key name for the object from parameters.
        :param has_active:      False if no active parameter, The Constant.active value if it does.
        :param allowed_items:   A list of items allowed to surface, anything not in this list will
                                be ignored.
        :param item_class:      The class used to instantiate individual items.
        """

        self._cfg_fn = cfg_fn
        self._cfg_root = cfg_root
        self._key_name = key_name
        self._has_active = has_active
        self._allowed_items = allowed_items
        self._item_class = item_class
        self._overrides = overrides

    @property
    def raw_items(self):

        cfg = self._cfg_fn()
        items = cfg[self._cfg_root]
        logging.debug(u'Raw Items: {e}'.format(e=items))

        # Return a copy so that modifications of the retrieved do not get saved in config unless explicitly requested!
        return deepcopy(items)

    def _items(self,
               active_only=False,
               include_hidden=False):

        items = {}

        for item_name, item_config in iteritems(self.raw_items):

            if self._allowed_items is not None:
                if item_name not in self._allowed_items:
                    # Item is not in allowed_items filter so we should not make it available.
                    continue

            if active_only and self._has_active and not item_config[self._has_active]:
                # Item not active and we want active items only
                continue

            if item_config is None:
                item_config = {}

            # Its expected that we only get a dict here.
            item_config[self._key_name] = item_name

            # Suppress items with a 'hidden' param = True if include_hidden is False.
            if item_config.get(u'hidden', False) and not include_hidden:
                continue

            items[item_name] = self.load_item(key=item_name,
                                              **self._overrides)

        return items

    def __getitem__(self, item):
        return self._items()[item]

    def __getattr__(self, item):
        try:
            return self.__getitem__(item)

        except KeyError:
            raise AttributeError(u'{name} does not have attribute {i}'.format(name=self.__class__.__name__,
                                                                              i=item))

    def __iter__(self):
        return iter(self._items())

    def __len__(self):
        return len(self._items())

    def load_item(self,
                  key,
                  **overrides):
        return self._item_class(cfg_fn=self._cfg_fn,
                                cfg_root=self._cfg_root,
                                key=key,
                                key_name=self._key_name,
                                **overrides)

    @deprecated
    def get_items(self,
                  active_only=False,
                  include_hidden=False):
        return [self[item] for item in self._items(active_only=active_only,
                                                   include_hidden=include_hidden)]

    @deprecated
    def get_item(self,
                 item,
                 active_only=False,
                 include_hidden=False,
                 suppress_refetch=False):

        # Check whether we have been passed an item which matches our item class
        # This may happen in which case we will either return or update it.
        if isinstance(item, self._item_class):
            if suppress_refetch:
                return item

            # Set item to its key ready for re-fetch
            item = item.key

        # Attempt to Fetch item directly
        try:
            return self[item]

        except KeyError:
            pass

        # We couldn't get the item directly so lets use some fuzzy logic
        for i in self.get_items(active_only=active_only,
                                include_hidden=include_hidden):
            # We've not found the item based on the key field so lets check all
            # additional attributes for item reference.
            for attribute in i.keys():
                if not attribute == u'inherits':
                    if i[attribute] == item:
                        return i

        raise LookupError(u'Unable to find item: {item}'.format(item=item))

    def get_active_items(self):
        return [self[item] for item in self._items(active_only=True)]

    def get_active_item(self,
                        item):
        return self._items(active_only=True)[item]

    def get_hidden_items(self):
        return [self[item] for item in self._items(include_hidden=True)]

    def get_hidden_item(self,
                        item):
        return self._items(include_hidden=True)[item]

    def get_item_by_key(self,
                        key,
                        value):

        items = [self[item] for item in self if self[item].get(key) == value]

        if len(items) == 1:
            return items[0]

        elif len(items) == 0:
            raise LookupError(u'Could not find an item with the key/value combination: {key} = {value}'
                              .format(key=key,
                                      value=value))
        else:
            raise LookupError(u'More than one item is configured with the key/value combination: {key} = {value}'
                              .format(key=key,
                                      value=value))

    def add(self,
            key_attr,
            config):

        # Remove key parameter
        if key_attr in config:
            del config[key_attr]

        cfg = self._cfg_fn()
        key = u'{c}.{i}'.format(c=self._cfg_root,
                                i=key_attr)

        cfg[key] = config

    def delete(self,
               key_attr):

        cfg = self._cfg_fn()
        key = u'{k}.{d}'.format(k=self._cfg_root,
                                d=key_attr)

        _ = cfg[self._cfg_root]
        del cfg[key]
