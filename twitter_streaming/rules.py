import requests
from .authorization import AuthorizationHeader
import json

'''
In order to get tweets for the topic that we desire, we need to first send the topic to the twitter.
If there is an existing topic, we need to delete it so that we can feed in the new topic.
'''

class Rules:
    def post_rules(self, rule):
        # Posting rules to the Twitter API
        auth = AuthorizationHeader()
        bearer_header = auth.bearer_header()
        final_rule = {"add":rule}
        print(final_rule)
        set_rules = requests.post("https://api.twitter.com/2/tweets/search/stream/rules", headers=bearer_header, json=final_rule)

        if set_rules.status_code != 201:
            raise Exception("Could not write rule....")
        return json.dumps(set_rules.json())

    def delete_rules(self, rules):
        # Deleting rules from the Twitter API
        auth = AuthorizationHeader()
        bearer_header = auth.bearer_header()
        final_rule = {"delete":{"ids":rules}}
        delete_rules = requests.post("https://api.twitter.com/2/tweets/search/stream/rules", headers=bearer_header, json=final_rule)

        if delete_rules.status_code != 200:
            raise Exception("Could not delete rule....")
        return json.dumps(delete_rules.json())
    
    def get_rules(self):
        # Getting rules from Twitter API
        auth = AuthorizationHeader()
        bearer_header = auth.bearer_header()

        set_rules = requests.get("https://api.twitter.com/2/tweets/search/stream/rules", headers=bearer_header)

        if set_rules.status_code != 200:
            print(json.dumpsset_rules)
            raise Exception("Could not get rules....")
        return json.dumps(set_rules.json())