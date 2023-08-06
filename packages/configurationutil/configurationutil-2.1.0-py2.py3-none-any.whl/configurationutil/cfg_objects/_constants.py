# encoding: utf-8

import attr

__all__ = ['DefaultInheritableConstant']


# Config Constants
@attr.s(frozen=True)
class _DefaultInheritableConstant(object):
    name = attr.ib(default=u'name', init=False)
    inherits = attr.ib(default=u'inherits', init=False)
    hidden = attr.ib(default=u'hidden', init=False)
    defaults = attr.ib(default=u'defaults', init=False)


DefaultInheritableConstant = _DefaultInheritableConstant()
