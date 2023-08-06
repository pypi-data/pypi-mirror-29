# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 23:24:30 2013

@author: mel
"""

import os

from beatle.model import TComponent
from beatle.tran import DelayedMethod
from beatle.model.writer import writer

class Module(TComponent):
    """Implements a Module representation"""
    class_container = False
    folder_container = True
    diagram_container = True
    namespace_container = True
    function_container = True
    variable_container = True
    enum_container = True

    def __init__(self, **kwargs):
        """Initialization"""
        self._header = kwargs.get('header', None)
        self._source = kwargs.get('source', None)
        self._lastSrcTime = None
        self._lastHdrTime = None
        self._header_obj = None  # vincle with file
        self._source_obj = None  # vincle with file
        super(Module, self).__init__(**kwargs)
        self.ExportCppCodeFiles(force=True)

    def Delete(self):
        """Handle delete"""
        project = self.project
        super(Module, self).Delete()
        project.ExportCppCodeFiles(force=True)

    def get_kwargs(self):
        """Returns the kwargs needed for this object"""
        return super(Module, self).get_kwargs()

    def OnUndoRedoAdd(self):
        """Update from app"""
        super(Module, self).OnUndoRedoAdd()
        self.ExportCppCodeFiles()

    def OnUndoRedoChanged(self):
        """Update from app"""
        super(Module, self).OnUndoRedoChanged()
        self.ExportCppCodeFiles()

    def OnUndoRedoRemoving(self):
        """Handle OnUndoRedoRemoving, prevent generating files"""
        self.ExportCppCodeFiles()
        super(Module, self).OnUndoRedoRemoving()

    @DelayedMethod()
    def ExportCppCodeFiles(self, force=True):
        """Do code generation"""
        self.updateSources(force)
        self.updateHeaders(force)

    def WriteCode(self, pf):
        """Write code for module"""
        #first the variables
        for variable in self.variables:
            variable.WriteCode(pf)
        #next functions
        for function in self.functions:
            function.WriteCode(pf)

    def updateSources(self, force=False):
        """does source generation"""
        sources_dir = self.project.sources_dir
        fname = os.path.realpath(os.path.join(sources_dir, self._source))
        regenerate = False
        if force or not os.path.exists(fname) or self._lastSrcTime is None:
            regenerate = True
        elif os.path.getmtime(fname) < self._lastSrcTime:
            regenerate = True
        if not regenerate:
            return
        f = open(fname, 'w')
        pf = writer.for_file(f)
        #master include file
        prj = self.project

        pf.writeln("// {user.before.include.begin}")
        pf.writeln(getattr(self, "user_code_s1",""))
        pf.writeln("// {user.before.include.end}")
        pf.writenl()
        if prj._useMaster:
            pf.writeln('#include "{0}"'.format(prj._masterInclude))
        else:
            pf.writeln('#include "{0}.h"'.format(self._header))
        pf.writenl()
        pf.writeln("// {user.before.code.begin}")
        pf.writeln(getattr(self, "user_code_s2",""))
        pf.writeln("// {user.before.code.end}")
        pf.writenl()
        self.WriteCode(pf)
        pf.writenl()
        pf.writeln("// {user.after.code.begin}")
        pf.writeln(getattr(self, "user_code_s3",""))
        pf.writeln("// {user.after.code.end}")
        pf.writenl()
        f.close()

    def updateHeaders(self, force=False):
        """Realiza la generacion de fuentes"""
        headers_dir = self.project.headers_dir

        fname = os.path.realpath(os.path.join(headers_dir, self._header))
        regenerate = False
        if force or not os.path.exists(fname) or self._lastHdrTime is None:
            regenerate = True
        elif os.path.getmtime(fname) < self._lastHdrTime:
            regenerate = True
        if not regenerate:
            return
        f = open(fname, 'w')
        pf = writer.for_file(f)
        inlines = []
        #create safeguard
        safeguard = self._header.upper() + "_INCLUDED"
        safeguard = safeguard.replace('.','_')
        pf.writeln("#if !defined({0})".format(safeguard))
        pf.writeln("#define {0}".format(safeguard))

        #we are using master include? if not, include inheritances
        pf.writenl()
        #ok, now we place comments, if any
        if len(self._note) > 0:
            pf.writeln("/**")
            txt = self._note
            txt.replace('\r', '')
            lines = txt.split("\n")
            for line in lines:
                line.replace('*/', '* /')
                pf.writeln("* {0}".format(line))
            pf.writeln("**/")
        #write variables (not static)

        pf.writenl()

        #first the variables
        for variable in self.variables:
            if not variable._static:
                variable.WriteDeclaration(pf)
                
        pf.writenl()
        
        #next functions
        for function in self.functions:
            function.WriteDeclaration(pf)

        #write methods

        pf.writenl()
        #end safeguard
        pf.writeln("#endif //{0}".format(safeguard))
        #write inlines
        pf.writenl()
        if len(inlines) > 0:
            pf.writeln("#if defined(INCLUDE_INLINES)")
            pf.writeln("#if !defined(INCLUDE_INLINES_{name})".format(name=self._header.upper()))
            pf.writeln("#define INCLUDE_INLINES_{name}".format(name=self._header.upper()))
            pf.writenl()
            #write inlines here

            pf.writeln("#endif //(INCLUDE_INLINES_{name})".format(name=self._header.upper()))
            pf.writeln("#endif //INCLUDE_INLINES")
            pf.writenl()
        self._lastHdrTime = os.path.getmtime(fname)

        pf.writenl()
        f.close()

    @property
    def bitmap_index(self):
        """Index of tree image"""
        from beatle.app import resources as rc
        return rc.GetBitmapIndex("module")

    @property
    def inner_class(self):
        """Get the innermost class container"""
        return None

