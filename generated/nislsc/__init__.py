"""Control NI SLSC hardware through Python.

This package provides a Python interface for NI SLSC hardware. Import
the main classes to interact with SLSC devices, sessions, properties,
and commands.

Aliases
-------

The top-level ``nislsc`` package provides aliases for commonly used classes:

- :class:`nislsc.Command <nislsc.command.Command>`: Open and execute SLSC device and physical channel commands.
- :class:`nislsc.Library <nislsc.library.Library>`: Initialize and manage the SLSC library interface.
- :class:`nislsc.Property <nislsc.property.Property>`: Access SLSC property references and configuration settings.
- :class:`nislsc.Session <nislsc.session.Session>`: Establish sessions with SLSC devices, channels, and NVMEM areas.
"""

from nislsc.command import Command
from nislsc.library import Library
from nislsc.property import Property
from nislsc.session import Session

__all__ = ["Command", "Library", "Property", "Session"]
