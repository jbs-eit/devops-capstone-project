import logging
from unittest import TestCase
from flask import Flask

from service.common.log_handlers import init_logging


class TestLogHandlers(TestCase):
    """Tests for log handlers"""

    def test_init_logging_sets_formatter_on_handlers(self):
        """It should set the formatter on all app logger handlers"""

        app = Flask("test-app")

        # Give the app logger at least one handler to format
        test_handler = logging.StreamHandler()
        app.logger.handlers = [test_handler]

        # Ensure there's a logger with handlers to copy from
        logger_name = "gunicorn.error"
        gunicorn_logger = logging.getLogger(logger_name)
        gunicorn_logger.handlers = [test_handler]
        gunicorn_logger.setLevel(logging.INFO)

        # Call function under test
        init_logging(app, logger_name)

        # Assert: every handler has a formatter with the expected format
        self.assertGreater(len(app.logger.handlers), 0)
        for handler in app.logger.handlers:
            self.assertIsNotNone(handler.formatter)
            self.assertEqual(
                handler.formatter._fmt,
                "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s",
            )
