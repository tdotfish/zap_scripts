# Note: This was a script that I wrote to quickly accomplish an objective but it is
# not great because it does not handle multi-select appropriately and it constantly
# switches over to the Script Output tab even though there is really nothing useful
# printed in there.
#
# I encourage you to use extender/sendtopostman_popup.py script instead but I'm
# leaving this script in github because the framework of building an OS command and
# running it could be helpful.
# 
# Translated the built-in curl_command_generator.js to python
# and tweaked it slightly so that you can right click a request in the History
# or other tab and send it to Postman to easily add it to a collection
#
# Usage: Put this script in `targeted`. Set the postmanPort variable as needed (default is 5555).
# Set Postman to capture requests.
# Then, right click a request and choose Invoke With Script... and then sendtopostman.py.

import os
import json

postmanPort=5555

def invokeWith(msg):
    cmd = "curl -i -s -k -x 'http://localhost:"+str(postmanPort)+"' -X  '"+msg.getRequestHeader().getMethod()+"'  \\\n"
    header = msg.getRequestHeader().getHeadersAsString()
    header = header.split(msg.getRequestHeader().getLineDelimiter())
    for i in header:
        keyval = i.split(":")
        if(keyval[0].strip() != "Host"):
            if i.strip():
                cmd = cmd + " -H '"+i.strip()+"' "
    cmd = cmd + "\\\n"
    body = msg.getRequestBody().toString()
    if body:
        cmd = cmd + "--data-binary $'"+json.dumps(body)[1:-1]+"' \\\n"
    cmd = cmd + "'"+msg.getRequestHeader().getURI().toString()+"'"
    result = os.system(cmd)
    print(result)
