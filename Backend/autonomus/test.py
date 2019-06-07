from autonomus.models import Link
import json
from google.cloud import datastore

def main():


    global client
    client = datastore.Client(project="autonomus", namespace="development")

    linkuri = list(Link.all())
    if len(linkuri) == 0:
        print('no links')
    else:
        last=[]
        for l in linkuri:
            last.append( l.follow_link)
        print(json.dumps(last))



if __name__ == "__main__":
    main()