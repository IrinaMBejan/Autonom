import logging
import random
import sys

from google.cloud import datastore
from autonomus.models import Tag


def test_model():
    # This is how to create a model instance
    tag = Tag(name="Frontend")

    # When doing put, you save it to datastore and get its identifier
    key = tag.put()
    print("Tag with key", key)

    # Urlsafe is another identifier
    usafe = tag.urlsafe
    print("urlsafe", usafe)

    # This is how you can retrieve an instance based on urlsafe
    tag = Tag.get(usafe)
    print("tag", tag)

    # Remove an instance of a model
    tag.remove()

    # Retrieve all items of a kind (.all)
    print("removed; remaining", Tag.all(keys_only=True))


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} FUNC")
        return

    global client
    client = datastore.Client(project="autonomus", namespace="development")

    funcs = {
        "test_model": test_model,
    }
    funcs[sys.argv[1]]()


if __name__ == "__main__":
    main()

# Example: $ python dstore.py test_model

