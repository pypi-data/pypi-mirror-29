# -*- Mode: Python; py-indent-offset: 4 -*-
# vim: tabstop=4 shiftwidth=4 expandtab
#
# Copyright (C) 2005-2009 Johan Dahlin <johan@gnome.org>
#               2015 Christoph Reiter
#
#   importer.py: dynamic importer for introspected libraries.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

from __future__ import absolute_import
import sys
import warnings
import importlib
from contextlib import contextmanager

import gi
from ._gi import Repository, RepositoryError
from ._gi import PyGIWarning
from .module import get_introspection_module
from .overrides import load_overrides


repository = Repository.get_default()

# only for backwards compatibility
modules = {}


@contextmanager
def _check_require_version(namespace, stacklevel):
    """A context manager which tries to give helpful warnings
    about missing gi.require_version() which could potentially
    break code if only an older version than expected is installed
    or a new version gets introduced.

    ::

        with _check_require_version("Gtk", stacklevel):
            load_namespace_and_overrides()
    """

    was_loaded = repository.is_registered(namespace)

    yield

    if was_loaded:
        # it was loaded before by another import which depended on this
        # namespace or by C code like libpeas
        return

    if namespace in ("GLib", "GObject", "Gio"):
        # part of glib (we have bigger problems if versions change there)
        return

    if gi.get_required_version(namespace) is not None:
        # the version was forced using require_version()
        return

    version = repository.get_version(namespace)
    warnings.warn(
        "%(namespace)s was imported without specifying a version first. "
        "Use gi.require_version('%(namespace)s', '%(version)s') before "
        "import to ensure that the right version gets loaded."
        % {"namespace": namespace, "version": version},
        PyGIWarning, stacklevel=stacklevel)


def get_import_stacklevel(import_hook):
    """Returns the stacklevel value for warnings.warn() for when the warning
    gets emitted by an imported module, but the warning should point at the
    code doing the import.

    Pass import_hook=True if the warning gets generated by an import hook
    (warn() gets called in load_module(), see PEP302)
    """

    py_version = sys.version_info[:2]
    if py_version <= (3, 2):
        # 2.7 included
        return 4 if import_hook else 2
    elif py_version == (3, 3):
        return 8 if import_hook else 10
    elif py_version == (3, 4):
        return 10 if import_hook else 8
    else:
        # fixed again in 3.5+, see https://bugs.python.org/issue24305
        return 4 if import_hook else 2


class DynamicImporter(object):

    # Note: see PEP302 for the Importer Protocol implemented below.

    def __init__(self, path):
        self.path = path

    def find_module(self, fullname, path=None):
        if not fullname.startswith(self.path):
            return

        path, namespace = fullname.rsplit('.', 1)
        if path != self.path:
            return

        # is_registered() is faster than enumerate_versions() and
        # in the common case of a namespace getting loaded before its
        # dependencies, is_registered() returns True for all dependencies.
        if repository.is_registered(namespace) or \
                repository.enumerate_versions(namespace):
            return self
        else:
            raise ImportError('cannot import name %s, '
                              'introspection typelib not found' % namespace)

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]

        path, namespace = fullname.rsplit('.', 1)

        stacklevel = get_import_stacklevel(import_hook=True)
        with _check_require_version(namespace, stacklevel=stacklevel):
            try:
                introspection_module = get_introspection_module(namespace)
            except RepositoryError as e:
                raise ImportError(e)
            # Import all dependencies first so their init functions
            # (gdk_init, ..) in overrides get called.
            # https://bugzilla.gnome.org/show_bug.cgi?id=656314
            for dep in repository.get_immediate_dependencies(namespace):
                importlib.import_module('gi.repository.' + dep.split("-")[0])
            dynamic_module = load_overrides(introspection_module)

        dynamic_module.__file__ = '<%s>' % fullname
        dynamic_module.__loader__ = self
        sys.modules[fullname] = dynamic_module

        return dynamic_module
