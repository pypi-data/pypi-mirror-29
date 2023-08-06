from NodeDefender.manage.setup import (manager, print_message, print_topic,
                                       print_info)
from flask_script import prompt
import NodeDefender


supported_brokers = ['amqp', 'redis']

@manager.command
def celery():
    print_topic("Celery")
    print_info("Celery is used for concurrent operation. It will spawn multiple\
               workes on multiple CPU cores and possibly even on multiple\
               hosts, running as a cluster. Disabling Celery will make\
               NodeDefender as a single process. Celery requires AMQP or Redis\
               to communicate between workes")
    enabled = None
    while enabled is None:
        enabled = prompt("Enable Celery(Y/N)").upper()
        if 'Y' in enabled:
            enabled = True
        elif 'N' in enabled:
            enabled = False
        else:
            enabled = None
    if not enabled:
        NodeDefender.config.celery.set(enabled = False)
        if NodeDefender.config.celery.write():
            print_info("Celery- config successfully written")
        return True
    
    broker = None
    while broker is None:
        broker = prompt("Enter Broker type(AMQP or Redis)").lower()
        if broker not in supported_brokers:
            broker = None

    host = None
    while host is None:
        host = prompt("Enter Server Address")

    port = None
    while port is None:
        port = prompt("Enter Server Port")

    database = ''
    while not database:
        database = prompt("Enter Database")

    server_name = ""
    while not server_name:
        print_info("Server name is needed for generating same URL")
        print_info("Format should be HOST or HOST:PORT")
        server_name = prompt("Enter Server name")
    NodeDefender.config.celery.set(enabled=True,
                                   broker=broker,
                                   host=host,
                                   port=port,
                                   database=database,
                                  server_name=server_name)
    if NodeDefender.config.celery.write():
        print_info("Celery- config successfully written")
    return True
