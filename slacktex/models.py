import json
import os
import requests
from urllib import quote


class Slack:
    def __init__(self):
        self.BASE_URL = "https://slack.com/api"
        self.API_TOKEN = os.environ.get("SLACK_API_TOKEN")
        self.SLASH_COMMAND_TOKEN = os.environ.get("SLACK_SLASH_COMMAND_TOKEN")

    def find_user_info(self, user_id):
        url = self.BASE_URL + "/users.info?token={0}&user={1}".format(
            self.API_TOKEN, user_id)
        response = requests.get(url)

        user = response.json().get("user")
        username = user["name"]
        icon_url = user["profile"]["image_48"]

        return {"username": username, "icon_url": icon_url}

    def post_latex_message(self, request):
        token = request.args.get("token")
        latex = request.args.get("text")
        channel_id = request.args.get("channel_id")
        user_id = request.args.get("user_id")
        response_url = request.args.get("response_url")

        if token != slack.SLASH_COMMAND_TOKEN:
            return "Unauthorized."

        latex = quote(latex)
        latex_url = "http://chart.apis.google.com/chart?cht=tx&chl={latex}".format(
            latex=latex)

        payload = {"channel": channel_id}
        user = self.find_user_info(user_id)
        payload.update(user)

        attachments = [{
            "image_url": latex_url,
            "fallback": "Oops. Something went wrong."
        }]
        payload.update({"attachments": attachments})

        requests.post(response_url, data=json.dumps(payload))
