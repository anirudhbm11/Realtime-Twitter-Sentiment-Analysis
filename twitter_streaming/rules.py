import requests
from .authorization import AuthorizationHeader
import json

class Rules:
    def post_rules(self, rule):
        auth = AuthorizationHeader()
        bearer_header = auth.bearer_header()
        final_rule = {"add":rule}
        print(final_rule)
        set_rules = requests.post("https://api.twitter.com/2/tweets/search/stream/rules", headers=bearer_header, json=final_rule)

        if set_rules.status_code != 201:
            raise Exception("Could not write rule....")
        return json.dumps(set_rules.json())
    
    def get_rules(self):
        auth = AuthorizationHeader()
        bearer_header = auth.bearer_header()

        set_rules = requests.get("https://api.twitter.com/2/tweets/search/stream/rules", headers=bearer_header)

        if set_rules.status_code != 200:
            print(json.dumpsset_rules)
            raise Exception("Could not get rules....")
        return json.dumps(set_rules.json())