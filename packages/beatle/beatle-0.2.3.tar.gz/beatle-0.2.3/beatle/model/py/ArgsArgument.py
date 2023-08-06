# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 22:31:28 2013

@author: mel
"""

import tran
from Argument import Argument


class ArgsArgument(Argument):
    """Implements argument representation"""

    context_container = True

    #visual methods
    @tran.TransactionalMethod('move argument {0}')
    def drop(self, to):
        """drop this elemento to another place"""
        target = to.inner_argument_container
        if not target or to.project != self.project:
            return False  # avoid move arguments between projects
        index = 0  # trick for insert as first child
        tran.TransactionalMoveObject(
            object=self, origin=self.parent, target=target, index=index)
        return True

    def __init__(self, **kwargs):
        """Initialization"""
        kwargs['name'] = 'args'
        kwargs['default'] = ''
        super(ArgsArgument, self).__init__(**kwargs)
        container = self.outer_class or self.outer_module
        container._lastSrcTime = None
        container._lastHdrTime = None

    @property
    def bitmap_index(self):
        """Index of tree image"""
        import app.resources as rc
        return rc.GetBitmapIndex('py_args')

    @property
    def label(self):
        """Get tree label"""
        return '*{self._name}'.format(self=self)

