# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright 2015-2018 by Exopy Authors, see AUTHORS for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# -----------------------------------------------------------------------------
"""Base classes to handle connection information edition.

Connection information are the information a user need to provide to open a
connection to an instrument. The format of a connection does not depend on the
architecture backend as any format discrepencies should be smoothed by the
starter used to instantiate the driver.

"""
from __future__ import (division, unicode_literals, print_function,
                        absolute_import)

from atom.api import Unicode, ForwardTyped, Bool
from enaml.core.api import d_, Declarative, d_func
from enaml.widgets.api import GroupBox


class BaseConnection(GroupBox):
    """Base widget for creating a connection.

    """
    #: Reference to the declaration that created this object.
    declaration = ForwardTyped(lambda: Connection)

    #: Whether or not to make the connection editable
    read_only = d_(Bool())

    @d_func
    def gather_infos(self):
        """Return the current values as a dictionary.

        """
        raise NotImplementedError()


class Connection(Declarative):
    """A declarative class for contributing a connection.

    Connection object can be contributed as extension children to the
    'connections' extension point of the 'exopy.instruments' plugin.

    """
    #: Unique name used to identify the connection.
    id = d_(Unicode())

    #: Connection description.
    description = d_(Unicode())

    @d_func
    def new(self, workbench, defaults, read_only):
        """Create a new connection and instantiate it properly.

        Defaults should be used to update the created connection.

        """
        raise NotImplementedError()
