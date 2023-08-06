# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 22:08:46 2013

@author: mel
"""
from beatle.model import TComponent, decorator
from beatle.ctx import THE_CONTEXT as context
from beatle.tran import TransactionStack, TransactionalMethod, TransactionalMoveObject


class Function(TComponent):
    """Implements member function"""
    context_container = True
    argument_container = True

    # visual methods
    @TransactionalMethod('move function {0}')
    def drop(self, to):
        """Drops datamember inside project or another folder """
        target = to.inner_function_container
        if not target or self.project != target.project:
            return False  # avoid move classes between projects
        index = 0
        TransactionalMoveObject(
            object=self, origin=self.parent, target=target, index=index)
        return True

    def __init__(self, **kwargs):
        """Initialization"""
        self._typei = kwargs['type']
        self._static = kwargs.get('static', False)
        self._inline = kwargs.get('inline', False)
        self._content = kwargs.get('content', "")
        self._template = kwargs.get('template', None)
        self._template_types = kwargs.get('template_types', [])
        super(Function, self).__init__(**kwargs)
        k = self.outer_class or self.outer_module
        if k:
            k.ExportCppCodeFiles(force=True)

    def Delete(self):
        """Handle delete"""
        k = self.outer_class or self.outer_module
        super(Function, self).Delete()
        if k:
            k.ExportCppCodeFiles(force=True)

    def get_kwargs(self):
        """Returns the kwargs needed for this object"""
        kwargs = {}
        kwargs['type'] = self._typei
        kwargs['static'] = self._static
        kwargs['inline'] = self._inline
        kwargs['content'] = self._content
        kwargs['template'] = self._template
        kwargs['template_types'] = self._template_types
        kwargs.update(super(Function, self).get_kwargs())
        return kwargs

    @decorator.ContextDeclaration()
    def WriteDeclaration(self, pf):
        """Write the member method declaration"""
        pf.writeln(self.declare)

    @decorator.ContextImplementation()
    def WriteCode(self, f):
        """Write code to file"""
        f.writenl(2)
        if len(self._note):
            f.opencomment()
            f.writeln(self._note)
            f.closecomment()
        f.writeln(self.implement)
        f.openbrace()
        f.writeln(self._content)
        f.closebrace()

    def OnUndoRedoChanged(self):
        """Update from app"""
        super(Function, self).OnUndoRedoChanged()
        if hasattr(self, '_pane') and not self._pane is None:
            book = context.frame.docBook
            index = book.GetPageIndex(self._pane)
            book.SetPageText(index, self.tab_label)
            book.SetPageBitmap(index, self.GetTabBitmap())
            if self._pane.m_editor.GetText() != self._content:
                self._pane.m_editor.SetText(self._content)
        if not TransactionStack.InUndoRedo():
            k = self.outer_class or self.outer_module
            if k:
                k.ExportCppCodeFiles(force=True)

    #def OnUndoRedoRemoving(self, root=True):
    def OnUndoRedoRemoving(self):
        """Prepare for delete"""
        if hasattr(self, '_pane') and not self._pane is None:
            book = context.frame.docBook
            p = self._pane
            delattr(self, '_pane')
            # we are not able to commit here!
            # pane.Commit()
            p.PreDelete()    # avoid gtk-critical
            self._paneIndex = book.GetPageIndex(p)
            book.DeletePage(self._paneIndex)
        #super(Function, self).OnUndoRedoRemoving(root)
        super(Function, self).OnUndoRedoRemoving()

    def OnUndoRedoAdd(self):
        """Restore object from undo"""
        from beatle.activity.models.ui.pane import MethodPane
        super(Function, self).OnUndoRedoAdd()
        if hasattr(self, '_paneIndex'):
            book = context.frame.docBook
            p = MethodPane(book, context.frame, self)
            self._pane = p
            book.InsertPage(self._paneIndex, p, self.tab_label,
                False, self.bitmap_index)
            delattr(self, '_paneIndex')

    def GetTabBitmap(self):
        """Get the bitmap for tab control"""
        from beatle.app import resources as rc
        return rc.GetBitmap("function")

    @property
    def bitmap_index(self):
        """Index of tree image"""
        from beatle.app import resources as rc
        return rc.GetBitmapIndex("function")

    @property
    def tab_label(self):
        """Get tree label"""
        from .Argument import Argument
        argl = ', '.join(arg.implement for arg in self[Argument])
        stype = (self._template and 'template<{0}> '.format(self._template)) or ''
        return "{stype}{name}({argl})".format(stype=stype, name=self._name, argl=argl)

    @property
    def tree_label(self):
        """Get tree label"""
        if self._template:
            stype = 'template<{0}> '.format(self._template)
        else:
            stype = ''
            if self._inline:
                stype = "inline " + stype
        stype += str(self._typei)
        from .Argument import Argument
        argl = ', '.join(arg.declare for arg in self[Argument])
        return stype.format(self._name + "(" + argl + ")")

    @property
    def declare(self):
        """Gets tab label"""
        from Argument import Argument
        s = str(self._typei)
        argl = ', '.join(arg.declare for arg in self[Argument])
        return s.format(" {self._name}({argl})".format(self=self, argl=argl)) + ";"

    @property
    def implement(self):
        """Gets tab label"""
        from Argument import Argument
        argl = ', '.join(arg.implement for arg in self[Argument])
        s = (self._template and 'template<{0}> '.format(self._template)) or ''
        s = s + str(self._typei)
        return s.format("{self.scope}{self._name}({argl})".format(self=self, argl=argl))

    def ExistArgumentNamed(self, name):
        """Returns information about argument existence"""
        from Argument import Argument
        return self.hasChild(name=name, type=Argument)

    @property
    def template_types(self):
        """Returns the list of nested template types"""
        lt = self._template_types
        nt = super(Function, self).template_types
        lt.extend([x for x in nt if x not in self._template_types])
        return lt
