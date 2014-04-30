import struct
from scarlett.constants import PRIORITY_NONE, PRIORITY_LOW, PRIORITY_HIGH
from scarlett.errors import ProtocolError
# Protocol specific constants
NULL_CHAR = '\x00'
MAGIC_RES_STRING = '%sRES' % NULL_CHAR
MAGIC_REQ_STRING = '%sREQ' % NULL_CHAR

## def get_command_name(cmd_type):
##     return SCARLETT_COMMAND_TO_NAME.get(cmd_type, cmd_type)


