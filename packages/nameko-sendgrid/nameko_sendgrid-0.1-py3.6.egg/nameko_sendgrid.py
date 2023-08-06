from nameko.extensions import DependencyProvider
from sendgrid import SendGridAPIClient


class SendGrid(DependencyProvider):
    def __init__(self, **options):
        self.options = options
        self.client = None
        self.key = None

    def setup(self):
        self.key = self.container.config["SENDGRID_KEY"]

    def start(self):
        self.client = SendGridAPIClient(apikey=self.key)

    def stop(self):
        self.client = None

    def kill(self):
        self.client = None

    def get_dependency(self, worker_ctx):
        return self.client
