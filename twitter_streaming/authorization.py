import os

class AuthorizationHeader:
    def bearer_header(self):
        # Store the Twitter Bearer token in system environment variable
        bearer_token = os.environ.get("twitter_bearer_token")
        return {"Authorization":"Bearer " + bearer_token}