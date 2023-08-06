# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 08:28:25 2013

@author: mel
"""


from beatle.model import TComponent
from beatle.tran import TransactionStack, TransactionalMoveObject, TransactionalMethod
from beatle.model import decorator as ctx


class Enum(TComponent):
    """Implements member data"""
    context_container = True

    #visual methods
    @TransactionalMethod('move enum {0}')
    def drop(self, to):
        """drop this elemento to another place"""
        if self.inner_class is None:
            return False
        target = to.inner_member_container
        if not target or to.project != self.project:
            return False  # avoid move arguments between projects
        index = 0  # trick for insert as first child
        TransactionalMoveObject(
            object=self, origin=self.parent, target=target, index=index)
        return True

    def __init__(self, **kwargs):
        """Initialization. The items argument is an optional list
        whose elements are a pair (label, value). """
        self._items = kwargs.get('items', [])
        self._access = kwargs.get('access', 'public')
        super(Enum, self).__init__(**kwargs)
        k = self.outer_class or self.outer_module
        if k:
            k.ExportCppCodeFiles(force=True)

    def Delete(self):
        """Handle delete"""
        k = self.outer_class or self.outer_module
        super(Enum, self).Delete()
        if k:
            k.ExportCppCodeFiles(force=True)

    def get_kwargs(self):
        """Returns the kwargs needed for this object"""
        kwargs = {}
        kwargs['items'] = self._items
        kwargs['access'] = self._access
        kwargs.update(super(Enum, self).get_kwargs())
        return kwargs

    @property
    def bitmap_index(self):
        """Index of tree image"""
        from beatle.app import resources as rc
        return rc.GetBitmapIndex("enum", self._access)

    def OnUndoRedoAdd(self):
        """Restore object from undo"""
        super(Enum, self).OnUndoRedoAdd()

    def OnUndoRedoChanged(self):
        """Make changes in the model as result of change"""
        super(Enum, self).OnUndoRedoChanged()
        if not TransactionStack.InUndoRedo():
            k = self.outer_class or self.outer_module
            if k:
                k.ExportCppCodeFiles(force=True)

    @property
    def scoped(self):
        """Get the scope"""
        return '{self.parent.scope}{self._name}'.format(self=self)

    @property
    def scope(self):
        """Get the scope"""
        return '{scoped}::'.format(scoped=self.scoped)

    @property
    def label(self):
        """Get tree label"""
        return 'enum {self._name}'.format(self=self)

    @ctx.ContextDeclaration()
    def WriteDeclaration(self, pf):
        """Write the declaration of the enum using writer"""
        cls = self.inner_class
        if cls is not None:
            cls._ensure_access(pf, self._access)
        #ok, write it
        self.WriteComment(pf)
        pf.writeln('enum {self._name}'.format(self=self))
        pf.openbrace()
        if len(self._items) > 0:
            for i in range(0, len(self._items) - 1):
                item = self._items[i]
                k = item[0].strip()
                s = item[1].strip()
                if len(s):
                    pf.writeln("{0}={1},".format(k, s))
                else:
                    pf.writeln("{0},".format(k))
            item = self._items[-1]
            k = item[0].strip()
            s = item[1].strip()
            if len(s):
                pf.writeln("{0}={1}".format(k, s))
            else:
                pf.writeln("{0}".format(k))
        pf.closebrace(";")


