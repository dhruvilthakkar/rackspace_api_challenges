# mailgun api key key-06pkah6xnmgqhu4tvkceplmo10kxot-1
#!/usr/bin/env python
import requests
from werkzeug import MultiDict

with open('/.mailgunapi','r') as f:
    key=f.readline()
print "key is: "+ key
def create_route():
    return requests.post(
        "https://api.mailgun.net/v2/routes",
        auth=("api", key),
        data= MultiDict([("priority", 1),
                        ("description", "Dhruvil's route"),
                        ("expression", "match_recipient('dhru4670@samples.mailgun.org')"),
                        ("action", "forward('http://cldsrvr.com/challenge1')"),
                        ("action", "stop()")]))

create_route()                       
