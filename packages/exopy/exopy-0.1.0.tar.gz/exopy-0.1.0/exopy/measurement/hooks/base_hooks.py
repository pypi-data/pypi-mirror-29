# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright 2015-2018 by Exopy Authors, see AUTHORS for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# -----------------------------------------------------------------------------
"""Base classes for all measurement hooks.

"""
from __future__ import (division, unicode_literals, print_function,
                        absolute_import)

from atom.api import Event

from ..base_tool import BaseMeasureTool, BaseToolDeclaration


class BaseExecutionHook(BaseMeasureTool):
    """Base class for all measurement hooks (pre or post execution).

    The execution management methods (pause, resume, stop) need to be
    implemented only if the execution of the hook is lengthy (this applies to
    hook executing tasks).

    """
    #: Event which the hook should fired (with a value of True) when it
    #: succeded to pause.
    paused = Event()

    #: Event which the hook should fired (with a value of True) when it
    #: succeded to resume.
    resumed = Event()

    def run(self, workbench, engine):
        """Perform additional operations before/after the measurement.

        This method can raise errors as necessary.

        Parameters
        ----------
        workbench : Workbench
            Reference to the application workbench.

        engine : Engine
            Active engine that can be used to execute tasks.

        """
        pass

    def pause(self):
        """Pause the execution of the hook.

        This call should not block waiting for the pause to occur. The paused
        signal should be fired once the pause is achieved.

        """
        pass

    def resume(self):
        """Resume the execution of the hook.

        This call should not block waiting for the resuming to occur. The
        resumed signal should be fired once the execution resumed.

        """
        pass

    def stop(self, force=False):
        """Stop the execution of the hook.

        This call should not block save if the force keyword is true. No signal
        is emitted as the run method should return as a result of the stop.

        """
        pass

    def list_runtimes(self, workbench):
        """List the runtimes dependencies for this hook.

        Parameters
        ----------
        workbench :
            Workbench of the application.

        Returns
        -------
        runtime : RuntimeContainer | None
            Runtime dependencies as returned by a call to the command
            'exopy.app.dependencies.analyse'. None means that the hook has no
            runtime dependency.

        """
        pass


class BasePreExecutionHook(BaseExecutionHook):
    """Base class for pre-execution measurement hooks.

    Notes
    -----
    This kind of hook can contribute entries to the task database. If it does
    so it should register those entries (add their name and a default value) at
    the root level of the database at linking time so that they appear in the
    autocompletion.

    """
    pass


class BasePostExecutionHook(BaseExecutionHook):
    """Base class for post-execution measurement hooks.

    """
    pass


class PreExecutionHook(BaseToolDeclaration):
    """A declarative class for contributing a measurement pre-execution.

    PreExecutionHook object can be contributed as extensions child to the
    'pre-execution' extension point of the 'exopy.measurement' plugin.

    """
    pass


class PostExecutionHook(BaseToolDeclaration):
    """A declarative class for contributing a measurement post-execution.

    PostExecutionHook object can be contributed as extensions child to the
    'post-execution' extension point of the 'exopy.measurement' plugin.

    """
    pass
