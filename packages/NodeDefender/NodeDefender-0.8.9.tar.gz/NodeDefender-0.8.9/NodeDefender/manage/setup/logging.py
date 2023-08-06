from NodeDefender.manage.setup import (manager, print_message, print_topic,
                                       print_info)
from flask_script import prompt
import NodeDefender


supported_engines = ['local', 'syslog']
supported_levels = ['debug', 'info', 'warning', 'error', 'critical']

@manager.command
def logging():
    print_topic("Logging")
    print_info("Logging to store runtime- information.")
    print_info("If disabled it will be printed to standard output")
    
    enabled = None
    while enabled is None:
        enabled = prompt("Enable Logging(Y/N)").upper()
        if 'Y' in enabled:
            enabled = True
        elif 'N' in enabled:
            enabled = False
        else:
            enabled = None

    if not enabled:
        NodeDefender.config.logging.set(enabled=False)
        if NodeDefender.config.logging.write():
            print_info("Logging- config successfully written")
        return False
    
    engine = None
    while engine is None:
        engine = prompt("Enter Logging Type(Syslog/Local)").lower()
        if engine not in supported_engines:
            engine = None
    
    filepath = None
    host=None
    port=None
    if engine == "local":
        while not filepath:
            print_info("Enter filename for loggingfile.")
            print_info("File will be stored in you datafolder")
            filepath = prompt("Please Filename")

    elif engine == "syslog":
        while not server:
            server = prompt('Enter Syslog IP')

        while not port:
            port = prompt('Enter Syslog Port')


    NodeDefender.config.logging.set(enabled=True,
                                    engine=engine,
                                    filepath=filepath,
                                    host=host,
                                    port=port,
                                    level="debug")
    if NodeDefender.config.logging.write():
        print_info("Logging- config successfully written")
    return True
