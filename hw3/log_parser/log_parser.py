import argparse
import os
import pathlib
import json
import re

PWD = str(pathlib.Path().absolute())

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', type=str, default='/access.log',
                    help='Input logfile name. Is "access.log" by default')
parser.add_argument('-s', '--searchpath', type=str, default=PWD,
                    help='Path to folder with your file. Is PWD by default')
parser.add_argument('-d', '--delimiter', type=str, default="\n***\n",
                    help='Delimiter for output elements. Is "\\n***\\n" by default')
parser.add_argument('-o', '--output', type=str, default=PWD,
                    help='Path to output file. Is "PWD/log_parser.out" by default')
parser.add_argument('-j', help='Save logs using json format', action='store_true')
parser.add_argument('-r', help='Save logs using json format', action='store_true')

args = parser.parse_args()
args.output += '/log_parser_py.out'

filepath = args.searchpath + args.filename


def parse_single_file(fname=filepath, fn=0):
    log_lines = []
    with open(fname) as log:
        for line in log:
            line = line.rstrip().split(" ")
            # Don't need time of request to count similar later
            del line[3]
            # Beautify method string
            line[4] = line[4][1:]
            log_lines.append(line)
    log.close()

    # Count requests count as number of lines in logfile
    NUM_OF_REQS = len(log_lines)

    # Count entries of distinct request types
    REQ_TYPES = {}
    for line in log_lines:
        if line[4] in REQ_TYPES:
            REQ_TYPES[line[4]] += 1
        else:
            REQ_TYPES[line[4]] = 1

    # Let's count similar requests despite time of request
    request_counter = {}
    counted_log_lines = []
    for line in log_lines:
        line = json.dumps(line)
        if line in request_counter:
            request_counter[line] += 1
        else:
            request_counter[line] = 1
    for request, count in request_counter.items():
        request = json.loads(request)
        request.insert(0, count)
        counted_log_lines.append(request)

    # Top 10 largest requests
    LARGEST = []
    counted_log_lines.sort(reverse=True, key=lambda column: int(column[9]))
    for i in range(0, 10):
        LARGEST.append([counted_log_lines[i][j] for j in [0, 6, 8]])

    # Top 10 frequent requests with code 4**
    user_error_log = [line for line in counted_log_lines if re.match(r"4..", line[8])]
    user_error_log.sort(reverse=True, key=lambda column: int(column[0]))
    FREQUENT = []
    for i in range(0, 10):
        FREQUENT.append([user_error_log[i][j] for j in [1, 6, 8]])

    # Top 10 largest requests with code 4**
    user_error_log.sort(reverse=True, key=lambda column: int(column[9]))
    LARGEST_ERR = []
    for i in range(0, 10):
        LARGEST_ERR.append([user_error_log[i][j] for j in [1, 6, 8]])

    # Save results to file
    output = args.output
    if args.r:
        output = output.replace('.out', '_' + str(fn) + '.out')
    if args.j:
        output = output.replace('.out', '.json')
        data = {'NUM_OF_REQS': [], 'COUNT BY METHOD': [], 'LARGEST': [], 'FREQUENT': [], 'LARGEST_ERR': []}
        data['NUM_OF_REQS'].append(
            {
                'TOTAL': NUM_OF_REQS
            }
        )
        data['COUNT BY METHOD'].append(
            REQ_TYPES
        )
        data['LARGEST'].append(
            json.dumps(LARGEST)
        )
        data['FREQUENT'].append(
            json.dumps(FREQUENT)
        )
        data['LARGEST_ERR'].append(
            json.dumps(LARGEST_ERR)
        )
        try:
            with open(output, 'w') as outfile:
                json.dump(data, outfile)
        except IOError as x:
            print(x)
    else:
        try:
            with open(output, 'w') as outfile:
                # 1
                outfile.write(str(NUM_OF_REQS))
                outfile.write(args.delimiter)
                # 2
                first = True
                for method in REQ_TYPES:
                    if first:
                        outfile.write(method + ' ' + str(REQ_TYPES[method]))
                        first = False
                    else:
                        outfile.write('\n' + method + ' ' + str(REQ_TYPES[method]))
                outfile.write(args.delimiter)
                # 3
                first = True
                for line in LARGEST:
                    if first:
                        outfile.write('\t'.join(str(x) for x in line))
                        first = False
                    else:
                        outfile.write('\n' + '\t'.join(str(x) for x in line))
                outfile.write(args.delimiter)
                # 4
                first = True
                for line in FREQUENT:
                    if first:
                        outfile.write('\t'.join(str(x) for x in line))
                        first = False
                    else:
                        outfile.write('\n' + '\t'.join(str(x) for x in line))
                outfile.write(args.delimiter)
                # 5
                first = True
                for line in LARGEST_ERR:
                    if first:
                        outfile.write('\t'.join(str(x) for x in line))
                        first = False
                    else:
                        outfile.write('\n' + '\t'.join(str(x) for x in line))
                outfile.close()
        except IOError as x:
            print(x)

    print("Done! Results are saved to file " + str(outfile.name))


if args.r:
    i = 0
    for filename in os.listdir(args.searchpath):
        print(filename)
        if filename.startswith('.'):
            pass
        else:
            parse_single_file(args.searchpath+filename, i)
            i += 1
else:
    parse_single_file()
