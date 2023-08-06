# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 22:08:46 2013

@author: mel
"""
from beatle.model.cc._MemberMethod import MemberMethod 
from beatle.tran import TransactionalMethod, TransactionalMoveObject


class IsClassMethod(MemberMethod):
    """Implements is_class method"""
    context_container = True
    argument_container = True

    # visual methods
    @TransactionalMethod('move is_class method {0}')
    def drop(self, to):
        """Drops datamember inside project or another folder """
        target = to.inner_member_container
        if not target or self.inner_class != target.inner_class or self.project != target.project:
            return False  # avoid move classes between projects
        index = 0
        TransactionalMoveObject(
            object=self, origin=self.parent, target=target, index=index)
        return True

    def __init__(self, **kwargs):
        """Initialization"""
        super(IsClassMethod, self).__init__(**kwargs)

    def get_kwargs(self):
        """Returns the kwargs needed for this object"""
        kwargs = {}
        kwargs.update(super(IsClassMethod, self).get_kwargs())
        return kwargs

    def OnUndoRedoChanged(self):
        """Update from app"""
        super(IsClassMethod, self).OnUndoRedoChanged()

    def OnUndoRedoRemoving(self):
        """Prepare for delete"""
        super(IsClassMethod, self).OnUndoRedoRemoving()

    def OnUndoRedoAdd(self):
        """Restore object from undo"""
        super(IsClassMethod, self).OnUndoRedoAdd()
