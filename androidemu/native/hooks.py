import logging

from androidemu.hooker import Hooker
from androidemu.native.memory import NativeMemory

from androidemu.java.helpers.native_method import native_method
from androidemu.utils import memory_helpers

logger = logging.getLogger(__name__)


class NativeHooks:

    """
    :type memory NativeMemory
    :type modules Modules
    :type hooker Hooker
    """
    def __init__(self, emu, memory, modules, hooker):
        self._emu = emu
        self._memory = memory

        modules.add_symbol_hook('__system_property_get', hooker.write_function(self.system_property_get) + 1)

    @native_method
    def system_property_get(self, uc, name_ptr, buf_ptr):
        name = memory_helpers.read_utf8(uc, name_ptr)
        logger.debug("Called __system_property_get(%s, 0x%x) was called" % (name, buf_ptr))

        if name in self._emu.system_properties:
            memory_helpers.write_utf8(uc, buf_ptr, self._emu.system_properties[name])
        else:
            raise ValueError('%s was not found in system_properties dictionary.' % name)

        return None

    @native_method
    def nop(self, emu):
        raise NotImplementedError()