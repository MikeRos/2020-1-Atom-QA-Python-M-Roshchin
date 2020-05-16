# NGINX Log parser (python and bash)
## How to use
Following info will be parsed and saved to output:
+ total number of requests
+ number of requests by method (GET - 20, POST - 10, etc.)
+ top 10 largest (sorted by log field $body_bytes_sent) requests (shows url, status, number of requests)
+ top 10 requests with user error in count (shows url, status, ip address)
+ top 10 largest (sorted by log field $body_bytes_sent) requests with user error (shows url, status, ip address)

To count similar requests request that differ only $time_local field are merged and counted

To see full usage guide use -h option
## Input
By default script will search for file named access.log in your PWD. To use custom path you should define
-s (searchpath) and/or -f (filename) parameters

+ -r option can be used to parse all files in "searchpath" directory

Scripts are designed to work with log files with following format
```
$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" "$http_x_forwarded_for"
```
Example
```
93.180.71.3 - - [17/May/2015:08:05:32 +0000] "GET /downloads/product_1 HTTP/1.1" 304 0 "-" "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"
```
## Output
Bash and python scripts output files format may differ
##### Little hint
######If top 10 largest requests differs in bash and python outputs, it means that there are more then 10 different requests with same size and largest requests tops are sorted in different ways  

Output is saved to file log_parser(_py).out

To customize the output you can use
+ -d (delimiter "\n***\n" by default)

and
+ -o (output)  path to output file. Is PWD by default

parameters

##### p.s.
Python script can form output as json file. Use -j option 

You can find examples of output files in this repo
