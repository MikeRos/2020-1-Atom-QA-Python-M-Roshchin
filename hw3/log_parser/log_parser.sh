#!/bin/bash

usage()
{
    echo
    echo "Syntax: log_parser.sh [-f filename] [-s path] [-d delimiter] [-o path]"
    echo "options:"
    echo "-f|--filename     Input logfile name. Is \"access.log\" by default"
    echo "-s|--searchpath   Path to folder with your file. Is PWD by default"
    echo "-d|--delimiter    Delimiter for output elements. Is \"\n***\n\" by default"
    echo "-o|--output       Path to output file. Is \"PWD/log_parser.out\" by default"
    echo
}

FILENAME="access.log"
SEARCHPATH=$PWD"/"
DELIMITER="\n***\n"
OUTPUT=$PWD/"log_parser.out"
while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        -h|--help|-"?")    # unknown option
        usage
        exit 1
        ;;
        -f|--filename)
        FILENAME="$2"
        shift # past argument
        shift # past value
        ;;
        -s|--searchpath)
        SEARCHPATH="$2"
        shift # past argument
        shift # past value
        ;;
        -d|-delimiter)
        DELIMITER="$2"
        shift # past argument
        shift
        ;;
        -o|--output)
        OUTPUT="$2"
        shift
        shift
        ;;
        *)    # unknown option
        echo "Unkwnown option: '$1'!"
        usage
        exit 1
        ;;
    esac
done

FILEPATH=$SEARCHPATH$FILENAME

if [ -r "$FILEPATH" ]; then
    true
else
    echo "Can't read input file or it does not exist"
    exit 1
fi

# Count requests count as number of lines in logfile
NUM_OF_REQS=$(wc "$FILEPATH" -l|awk '{ print $1 }')

# Count entries of distinct requset types
REQ_TYPES=$(awk '{ REQ_TYPES[$6]++} END {for (t in REQ_TYPES) print substr(t,2), REQ_TYPES[t] }' "$FILEPATH")

# Top 10 largest requests
LARGEST=$(sed -r 's/\[.*\] //' "$FILEPATH"|sort|uniq -c|sort -nk9|tail|sort -rnk9| awk '{print "URL: " $6 "\t Code: " $8 "\t Count: " $1}')

# Top 10 frequent requests with code 4**
FREQUENT_ERR=$(sed -r 's/\[.*\] //' "$FILEPATH"|awk 'match($7,/4../){ print }'|sort|uniq -c|sort -nk1|tail|sort -rnk1\
| awk '{print "URL: " $6 "\t Code: " $8 "\t IP: " $2}')

# Top 10 largest requests with code 4**
LARGEST_ERR=$(sed -r 's/\[.*\] //' "$FILEPATH"|awk 'match($7,/4../){ print }'|sort|uniq -c|sort -nk9|tail|sort -rnk9\
| awk '{print "URL: " $6 "\t Code: " $8 "\t IP: " $2}')

echo -e "$NUM_OF_REQS$DELIMITER$REQ_TYPES$DELIMITER$LARGEST$DELIMITER$FREQUENT_ERR$DELIMITER$LARGEST_ERR" > "$OUTPUT"
echo "Done! Results are saved into $OUTPUT"
exit 0