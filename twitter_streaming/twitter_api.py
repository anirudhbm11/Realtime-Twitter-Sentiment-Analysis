from .authorization import AuthorizationHeader
from .rules import Rules
import requests
import json

class TwitterStreamAPI:
    def get_stream(self, topics):
        print("\n Posting rules.....")
        self.post_rules(topics)
        print("\n Successfully posted rules")
        print("\n Starting to get stream data......")

        auth = AuthorizationHeader()
        bearer_header = auth.bearer_header()

        stream = requests.get("https://api.twitter.com/2/tweets/search/stream",headers=bearer_header,stream=True)

        if stream.status_code != 200:
            raise Exception("Error in calling stream")
        
        print("200 OK!")

        return stream

        # for response_line in stream.iter_lines():
        #     if response_line:
        #         json_response = json.loads(response_line)
        #         # publish_message(kafka_producer, 'twitter', 'raw', json_response)
        #         print(json.dumps(json_response, indent=4, sort_keys=True))

    def post_rules(self, rules_to_post):
        rules = Rules()
        get_rules = rules.get_rules()
        print("Original Rules: \n")
        print(get_rules)
        set_rules = rules.post_rules(rules_to_post)
        print("Rules after updaing:  \n")
        get_rules = rules.get_rules()


if __name__ == "__main__":
    topics = [
            {"value": "#ftx"},
            # {"value": "cat has:images -grumpy", "tag": "cat pictures"},
        ]

    stream_api = TwitterStreamAPI()
    stream_api.get_stream(topics)


