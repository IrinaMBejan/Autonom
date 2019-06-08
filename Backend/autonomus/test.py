from google.cloud import datastore
from autonomus.controllers import tags_controller
import os

def main():


    global client
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/andrei/autonomus.json"
    client = datastore.Client(project="autonomus", namespace="development")

    print(tags_controller.get_Tags('sports , music'))



if __name__ == "__main__":
    main()