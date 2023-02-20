from .authorization import AuthorizationHeader
from .rules import Rules
import requests
import json

class TwitterStreamAPI:
    def get_stream(self, topics):
        print("\n Posting rules.....")
        # self.post_rules(topics)
        print("\n Successfully posted rules")
        print("\n Starting to get stream data......")

        # Authenticating with the Twitter API
        auth = AuthorizationHeader()
        bearer_header = auth.bearer_header()

        stream = requests.get("https://api.twitter.com/2/tweets/search/stream",headers=bearer_header,stream=True)

        if stream.status_code != 200:
            raise Exception("Error in calling stream")

        return stream

    def post_rules(self, rules_to_post):
        # Deleting and posting new rules to the twitter for our desired topics.
        rules = Rules()
        get_rules = json.loads(rules.get_rules())
        data = get_rules["data"]
        original_rules = [element["id"] for element in data]
        rules.delete_rules(original_rules)
        rules.post_rules(rules_to_post)
        print("Posted new rules....")


if __name__ == "__main__":
    # Topic given for the purpose of testing
    topics = [
            {"value": "#ftx"},
        ]

    stream_api = TwitterStreamAPI()
    stream_api.get_stream(topics)


