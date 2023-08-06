# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 22:08:46 2013

@author: mel
"""
from beatle import tran
from beatle.ctx import get_context
from beatle.model import Member 
from beatle.model.decorator import ContextDeclaration, ContextImplementation


class MemberMethod(Member):
    """Implements member method"""
    context_container = True
    argument_container = True
    import_container = True

    # visual methods
    @tran.TransactionalMethod('move method {0}')
    def drop(self, to):
        """Drops datamember inside project or another folder """
        target = to.inner_member_container
        if not target or self.inner_class != target.inner_class or self.project != target.project:
            return False  # avoid move classes between projects
        index = 0
        tran.TransactionalMoveObject(
            object=self, origin=self.parent, target=target, index=index)
        return True

    def __init__(self, **kwargs):
        """Initialization"""
        from .Argument import Argument
        from .Decorator import Decorator
        self._staticmethod = kwargs.get('static_method', False)
        self._classmethod = kwargs.get('class_method', False)
        self._property = kwargs.get('property', False)
        self._content = kwargs.get('content', "")
        super(MemberMethod, self).__init__(**kwargs)
        if not self._staticmethod and not kwargs.get('raw', False):
            if self._property or not self._classmethod:
                if not self.ExistArgumentNamed('self'):
                    Argument(parent=self, name='self')
            else:
                if not self.ExistArgumentNamed('self'):
                    Argument(parent=self, name='cls')
        if self._staticmethod:
            self._staticmethod = Decorator(parent=self, name='staticmethod')
        if self._classmethod:
            self._classmethod = Decorator(parent=self, name='classmethod')
        if self._property:
            self._property = Decorator(parent=self, name='property')
        k = self.inner_module or self.inner_package
        if k:
            k.ExportPythonCodeFiles()

    def Delete(self):
        """Handle delete"""
        k = self.inner_module or self.inner_package
        super(MemberMethod, self).Delete()
        if k:
            k.ExportPythonCodeFiles()

    def get_kwargs(self):
        """Returns the kwargs needed for this object"""
        kwargs = {}
        kwargs['static_method'] = bool(self._staticmethod)
        kwargs['class_method'] = bool(self._classmethod)
        kwargs['property'] = bool(self._property)
        kwargs['content'] = self._content
        kwargs.update(super(MemberMethod, self).get_kwargs())
        return kwargs

    @ContextDeclaration()
    def WriteDeclaration(self, pf):
        """Write the member method declaration"""
        pass

    @ContextImplementation()
    def WriteCode(self, f):
        """Write code to file"""
        pass

    def OnUndoRedoChanged(self):
        """Update from app"""
        super(MemberMethod, self).OnUndoRedoChanged()
        if hasattr(self, '_pane') and not self._pane is None:
            context = get_context()
            book = context.frame.docBook
            index = book.GetPageIndex(self._pane)
            book.SetPageText(index, self.tab_label)
            book.SetPageBitmap(index, self.GetTabBitmap())
            if self._pane.m_editor.GetText() != self._content:
                self._pane.m_editor.SetText(self._content)

    def OnUndoRedoRemoving(self):
        """Prepare for delete"""
        if hasattr(self, '_pane') and not self._pane is None:
            context = get_context()            
            book = context.frame.docBook
            p = self._pane
            delattr(self, '_pane')
            p.Commit()
            p.PreDelete()    # avoid gtk-critical
            self._paneIndex = book.GetPageIndex(p)
            book.DeletePage(self._paneIndex)
        super(MemberMethod, self).OnUndoRedoRemoving()

    def OnUndoRedoAdd(self):
        """Restore object from undo"""
        from beatle.activity.models.ui import pane
        super(MemberMethod, self).OnUndoRedoAdd()
        if hasattr(self, '_paneIndex'):
            context = get_context()
            book = context.frame.docBook
            p = pane.PyMethodPane(book, context.frame, self)
            self._pane = p
            book.InsertPage(self._paneIndex, p, self.tab_label,
                False, self.bitmap_index)
            delattr(self, '_paneIndex')

    def ExportPythonCode(self, wf):
        """Write code"""
        # first, write decorators, if any
        from .Decorator import Decorator
        for deco in self[Decorator]:
            deco.ExportPythonCode(wf)
        wf.openbrace(self.declare)
        wf.writecomment(self._note)
        wf.writeblock(self._content)
        wf.closebrace()
        wf.writenl()

    def GetTabBitmap(self):
        """Get the bitmap for tab control"""
        from beatle.app import resources as rc
        return rc.GetBitmap("py_method")

    @property
    def bitmap_index(self):
        """Index of tree image"""
        from beatle.app import resources as rc
        return rc.GetBitmapIndex("py_method")

    @property
    def tree_label(self):
        """Get tree label"""
        from .Argument import Argument
        from .ArgsArgument import ArgsArgument
        from .KwArgsArgument import KwArgsArgument
        alist = ', '.join(arg.label for arg in
            self[Argument] + self[ArgsArgument] + self[KwArgsArgument])
        return '{self._name}({alist})'.format(self=self, alist=alist)

    @property
    def tab_label(self):
        """Get tab label"""
        from .Argument import Argument
        from .ArgsArgument import ArgsArgument
        from .KwArgsArgument import KwArgsArgument
        alist = ', '.join(arg.label for arg in
            self[Argument] + self[ArgsArgument] + self[KwArgsArgument])
        return '{self._name}({alist})'.format(self=self, alist=alist)

    @property
    def declare(self):
        """Get tab label"""
        from .Argument import Argument
        from .ArgsArgument import ArgsArgument
        from .KwArgsArgument import KwArgsArgument
        alist = ', '.join(arg.label for arg in
            self[Argument] + self[ArgsArgument] + self[KwArgsArgument])
        return 'def {self._name}({alist}):'.format(self=self, alist=alist)

    def ExistArgumentNamed(self, name):
        """Check about the existence of an argument"""
        from .Argument import Argument
        from .ArgsArgument import ArgsArgument
        from .KwArgsArgument import KwArgsArgument
        return name in [x._name for x in self(Argument, ArgsArgument,
            KwArgsArgument)]

