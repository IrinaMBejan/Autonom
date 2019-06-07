from autonomus.models import Link
import requests

def exists_link(data_link):
    """Verify if a link exists in the datastore"""
    query = Link.query()
    query.add_filter('follow_link', '=', data_link)
    query_it = query.fetch()
    for ent in query_it:
        if ent is None:
            return None
        else :
            return ent

    return None

def check_link(data_link):
    request = requests.get(data_link)
    if request.status_code == 200:
        return True
    else:
        return False