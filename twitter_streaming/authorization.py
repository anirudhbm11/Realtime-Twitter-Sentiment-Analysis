import os

class AuthorizationHeader:
    def bearer_header(self):
        # bearer_token = os.environ.get("twitter_bearer")
        bearer_token = "AAAAAAAAAAAAAAAAAAAAAGAkigEAAAAApKiVyFfDRYeJphU49dUfqC3e2cY%3Dmnkb2oCZBr7VdsuMBZzOGR9OMWtOnD3pS2Ap9bKjeixAWo7HfO"
        return {"Authorization":"Bearer " + bearer_token}