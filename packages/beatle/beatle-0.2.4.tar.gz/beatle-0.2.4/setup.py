import os
from setuptools.command.install import install
from setuptools import setup, find_packages

class extra_install(install):

	user_options = install.user_options + [('reinstall-wxpython', None, 'rebuild and reinstall wxpython')]

	def initialize_options(self):
		install.initialize_options(self)
		self.reinstall_wxpython = False

	def run(self):
		install.run(self)
		import sys
		#check about wxwidgets
		try:
                        assert not self.reinstall_wxpython
			import wxversion
			wxversion.select('3.0')
		except:
			with open('install-wxpython.sh', 'w') as shell_script:
				shell_script.write("""#!/bin/sh
				echo 'Prerrequisites'
				apt-get --yes --force-yes install libgconf2-dev libgtk2.0-dev libgtk-3-dev mesa-common-dev libgl1-mesa-dev libglu1-mesa-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev libgconfmm-2.6-dev libwebkitgtk-dev python-gtk2
				mkdir -p external
				cd external
				echo "Downloading wxPython 3.0.2.0"
				wget http://downloads.sourceforge.net/project/wxpython/wxPython/3.0.2.0/wxPython-src-3.0.2.0.tar.bz2
				echo "Done"
				echo 'Uncompressing ...'
				tar -xjvf wxPython-src-3.0.2.0.tar.bz2
				echo 'Patching  ...'
				cd wxPython-src-3.0.2.0
				sed -i '1i \#include <math.h>\' ./src/stc/scintilla/src/Editor.cxx
				cd wxPython
				sed -i -e 's/PyErr_Format(PyExc_RuntimeError, mesg)/PyErr_Format(PyExc_RuntimeError, "%s\", mesg)/g' src/gtk/*.cpp contrib/gizmos/gtk/*.cpp
				python ./build-wxpython.py --build_dir=../bld --install
				ldconfig
				cd ../../..
				rm -rf external
			""")
			os.system("sh ./install-wxpython.sh")

def ftext(filename):
	"""Quick utility for reading a text file"""
	return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
	name = 'beatle',
	version = '0.2.4',
	author = 'mel viso',
	author_email = 'melviso@telefonica.net',
	url = 'https://github.com/melviso/beatle',
	description = ('A development environment made in python'),
	license = 'GNU Public License',
	keywords = 'development python c++',
	long_description=ftext('README'),
	classifiers = [
		"Intended Audience :: Developers",
		"Development Status :: 2 - Pre-Alpha",
		"Topic :: Utilities",
		"License :: OSI Approved :: GNU General Public License (GPL)",
		"Natural Language :: English",
		"Operating System :: POSIX :: Linux",
		"Programming Language :: Python :: 2.7",
		"Topic :: Software Development :: Code Generators",
	],
	package_data = {'':['beatle/app/res/*.xpm','beatle/app/res/*.jpg','beatle/app/res/*.gif', 'beatle/plugin/models/relation/standard/*.xml'],},
	include_package_data=True,
	packages=[
		'beatle',
		'beatle.activity',
		'beatle.activity.arch',
		'beatle.activity.arch.actions',
		'beatle.activity.arch.handlers',
		'beatle.activity.arch.handlers.cpp',
		'beatle.activity.arch.handlers.py',
		'beatle.activity.arch.handlers.text',
		'beatle.activity.arch.ui',
		'beatle.activity.arch.ui.dlg',
		'beatle.activity.arch.ui.view',
		'beatle.activity.arch.ui.pane',
		'beatle.activity.git',
		'beatle.activity.git.ui',
		'beatle.activity.git.ui.dlg',
		'beatle.activity.git.ui.view',
		'beatle.activity.models',
		'beatle.activity.models.handlers',
		'beatle.activity.models.handlers.cpp',
		'beatle.activity.models.handlers.gui',
		'beatle.activity.models.handlers.py',
		'beatle.activity.models.handlers.sql',
		'beatle.activity.models.ui',
		'beatle.activity.models.ui.dlg',
		'beatle.activity.models.ui.dlg.cc',
		'beatle.activity.models.ui.dlg.py',
		'beatle.activity.models.ui.pane',
		'beatle.activity.models.ui.view',
		'beatle.activity.targets',
		'beatle.activity.targets.ui',
		'beatle.activity.targets.ui.view',
		'beatle.activity.tasks',
		'beatle.activity.tasks.ui',
		'beatle.activity.tasks.ui.dlg',
		'beatle.activity.tasks.ui.view',
		'beatle.analytic',
		'beatle.analytic.sema',
		'beatle.app',
		'beatle.app.resources',
		'beatle.app.res',
		'beatle.app.res.16x16',
		'beatle.app.ui',
		'beatle.app.ui.ctrl',
		'beatle.app.ui.dlg',
		'beatle.app.ui.pane',
		'beatle.app.ui.tools',
		'beatle.app.ui.view',
		'beatle.builtin',
		'beatle.builtin.libraries',
		'beatle.builtin.libraries.stl',
		'beatle.builtin.libraries.stl.containers',
		'beatle.builtin.libraries.stl.utility',
		'beatle.ctx',
		'beatle.lib',
		'beatle.lib.decorators',
		'beatle.lib.handlers',
		'beatle.lib.wxx',
		'beatle.model',
		'beatle.model.cc',
		'beatle.model.checklist',
		'beatle.model.database',
		'beatle.model.decorator',
		'beatle.model.arch',
		'beatle.model.git',
		'beatle.model.py',
		'beatle.model.tasks',
		'beatle.model.writer',
		'beatle.lib.ostools',
		'beatle.pane',
		'beatle.plugin',
		'beatle.plugin.models',
		'beatle.plugin.models.relation',
		'beatle.plugin.models.relation.standard',
		'beatle.plugin.tools',
		'beatle.plugin.tools.ast_explorer',
		'beatle.plugin.tools.ast_explorer.res',
		'beatle.plugin.tools.log_explorer',
		'beatle.plugin.tools.web_browser',
		'beatle.plugin.tools.check_updates',
		'beatle.tran',
		],
	cmdclass={'install': extra_install},
	install_requires = ['PyPDF2', 'GitPython==2.0.8', 'trepan', 'python<3'], #'wxPython==4.0.0a2'],
	scripts=['script/beatle'],
)
	
	
