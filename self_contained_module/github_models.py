# GitHub Models handling logic


class GitHubModelsHandler:
    def __init__(self, retry_strategy):
        self.retry_strategy = retry_strategy

    def call_model(self, model_name, payload):
        # Logic to call GitHub Models with retry strategy
        pass

    def handle_rate_limit(self):
        # Logic to handle rate limits
        pass
