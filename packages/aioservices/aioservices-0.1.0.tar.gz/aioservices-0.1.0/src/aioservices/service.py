"""Aioservices - service."""


class AsyncService:
    """Asynchronous service."""

    def __init__(self, broker):
        """Initializer."""
        self.broker = broker

    def main(self):
        """Run service."""
        print('Main works')
