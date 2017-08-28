import json
import urllib2
import sys
from sets import Set

import time

url = "http://localhost:14265"
folder = './'


#Utils:
all_nines = '9' * 81
TIMEOUT = 7
def API(request,url=url):

    stringified = json.dumps(request)
    headers = {'content-type': 'application/json'}

    try:
        request = urllib2.Request(url=url, data=stringified, headers=headers)
        returnData = urllib2.urlopen(request,timeout=TIMEOUT).read()
        response = json.loads(returnData)

    except:
        print url, "Timeout!"
        print '\n    ' + repr(sys.exc_info())
        return " "
    if not response:
        response = " "
    return response

def getNodeInfo():
    cmd = {
        "command": "getNodeInfo"
    }
    return API(cmd)

def getTrytes(hash):
    cmd = {
        "command": "getTrytes",
        "hashes" : [hash]
    }
    return API(cmd)



# check that node is solid:
# and get latest milestone hash
solid_milestone = False
while not solid_milestone:
    node_info = getNodeInfo()
    if node_info['latestSolidSubtangleMilestone'] != all_nines:
        if node_info['latestSolidSubtangleMilestoneIndex'] == node_info['latestMilestoneIndex']:
            solid_milestone = node_info['latestSolidSubtangleMilestone']
            break
    print "waiting for node to get solid:" + str(node_info['latestSolidSubtangleMilestoneIndex']) + "/" + str(node_info['latestMilestoneIndex'])
    time.sleep(2)

#traverse the tangle from latest milestone, till all9
file = folder + node_info['appName'] + "_" + node_info['appVersion'] + "_" + str(node_info['latestSolidSubtangleMilestoneIndex']) + ".dmp"
memDB = Set()
traversal_queue = [solid_milestone]
counter = 0

with open(file,"w+") as f:
    while traversal_queue:
        tx_hash = traversal_queue.pop()
        if tx_hash in memDB or tx_hash == all_nines:
            continue

        #get transaction details
        try:
            tx = getTrytes(tx_hash)['trytes'][0]
        except:
            print "Error:",tx_hash
            exit(-1)

        # store transaction in file (and hash in memory, to avoid duplicates)
        memDB.add(tx_hash)
        f.write(tx_hash + "," + tx + "\n")
        counter += 1
        print "stored:",counter,tx_hash

        #add branch and trunk to queue
        trunk_transaction_hash  = tx[2430:2511]
        branch_transaction_hash = tx[2511:2592]
        traversal_queue.append(trunk_transaction_hash)
        traversal_queue.append(branch_transaction_hash)

pass

