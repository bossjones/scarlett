import scarlett
from scarlett.constants import *
from scarlett.errors import ProtocolError

# Protocol specific constants
NULL_CHAR = '\x00'
MAGIC_RES_STRING = '%sRES' % NULL_CHAR
MAGIC_REQ_STRING = '%sREQ' % NULL_CHAR

# def get_command_name(cmd_type):
# return SCARLETT_COMMAND_TO_NAME.get(cmd_type, cmd_type)


class Command(object):

    def __init__(self):
        self.config = scarlett.config

    def check_cmd(self, command=''):

        if command in SPOTIFY_CMDS.keys():
            scarlett.log.debug(Fore.YELLOW +
                "** received %s, sending 'spotify %s'" %
                (command, SPOTIFY_CMDS[command]))
            # REFACTOR ### spotify_play(SPOTIFY_CMDS[command])
        elif command in LIGHT_CMDS.keys():
            scarlett.log.debug(Fore.YELLOW +
                "** received %s, sending 'light %s'" %
                (command, LIGHT_CMDS[command]))
            try:
                scarlett.log.debug(Fore.YELLOW + "trying light chit")
                # REFACTOR ### light_play(LIGHT_CMDS[command])
            except Exception as e:
                scarlett.log.debug(Fore.YELLOW +
                    "light exception b. \nCMD: %s \nException: %s" %
                    (command, e))
                # REFACTOR ### general_play("cancel")
        elif command in TIME_CMDS.keys():
            scarlett.log.debug(Fore.YELLOW +
                "** received %s, sending 'time %s'" %
                (command, TIME_CMDS[command]))
            try:
                # REFACTOR ### time_play(TIME_CMDS[command])
                scarlett.log.debug(Fore.YELLOW + "I WOULD TELL THE TIME")
            except Exception as e:
                scarlett.log.debug(Fore.YELLOW +
                    "time exception b. \nCMD: %s \nException: %s" %
                    (command, e))
                # REFACTOR ### general_play("cancel")
        elif command in GENERAL_CMDS.keys():
            scarlett.log.debug(Fore.YELLOW +
                "** received %s, sending 'general command: %s'" %
                (command, GENERAL_CMDS[command]))
            # REFACTOR ### general_play(GENERAL_CMDS[command])
        elif command in FORECAST_CMDS.keys():
            scarlett.log.debug(Fore.YELLOW +
                "** received %s, sending 'forecast command: %s'" %
                (command, FORECAST_CMDS[command]))
            # REFACTOR ### forecast_play(FORECAST_CMDS[command])
        elif command in tv_commands.keys():
            scarlett.log.debug(Fore.YELLOW +
                "** received %s, sending 'tv command: %s'" %
                (command, tv_commands[command]))
            # REFACTOR ### tv_play(tv_commands[command])
