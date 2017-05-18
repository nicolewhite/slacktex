from flask import Flask, request
from models import Slack


app = Flask(__name__)


@app.route("/",  methods=['GET', 'POST'])
def index():
    print request
    if not request.args:
        message = """
        Welcome to SlackTeX!
        Check me out on <a href="https://github.com/nicolewhite/slacktex">GitHub</a>.
        """

        return message

    else:
        slack = Slack()
        slack.post_latex_message(request)

        return "Success!", 200
