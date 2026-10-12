
from unittest.mock import Mock, patch

from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.exceptions import ValidationError

from helpers.exceptions import custom_exception_handler


class TestCustomExceptionHandler(SimpleTestCase):
    def test_validation_error_keeps_400_status(self):
        exc = ValidationError({"name": ["This field is required."]})

        response = custom_exception_handler(exc, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"name": ["This field is required."]},
        )

    @patch("helpers.exceptions.logger.error")
    @patch("helpers.exceptions.exception_handler", return_value=None)
    def test_unexpected_exception_returns_generic_500(
        self, mock_handler, mock_logger
    ):
        exc = RuntimeError("Sensitive database connection details")
        context = {"view": Mock()}

        response = custom_exception_handler(exc, context)
        print("response", response)

        self.assertEqual(
            response.status_code,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        self.assertEqual(
            response.data,
            {
                "status": 0,
                "message": "An unexpected error occurred.",
            },
        )
        self.assertNotIn(
            "Sensitive database connection details",
            str(response.data),
        )
        mock_logger.assert_called_once()