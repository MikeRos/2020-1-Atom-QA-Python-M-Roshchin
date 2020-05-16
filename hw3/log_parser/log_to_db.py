import argparse
import pathlib
import shlex
from db.orm_builder import MysqlOrmLogBuilder
from db.orm_client import MysqlOrmConnection

PWD = str(pathlib.Path().absolute())

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', type=str, default='/access.log',
                    help='Input logfile name. Is "access.log" by default')
parser.add_argument('-s', '--searchpath', type=str, default=PWD,
                    help='Path to folder with your file. Is PWD by default')
args = parser.parse_args()
filepath = args.searchpath + args.filename

try:
    with open(filepath) as f:
        pass
except IOError as x:
    print(x)

log_lines = []
with open(filepath) as log:
    for line in log:
        line = shlex.split(line.rstrip())
        # Beautify method string
        line[4] = line[4][1:]
        log_lines.append(line)
log.close()

connection = MysqlOrmConnection('test', 'testpass', 'LOG_DB')
log_db = MysqlOrmLogBuilder(connection)
log_db.create_log_db()
log_db.add_log(log_lines)
log_db.connection.session.close()
