import logging

from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # DRF has already handled known API exceptions,
        # such as validation errors and permission errors.
        return response

    # Log unexpected exceptions internally, not in the API response.
    logger.error(
        "Unhandled API exception",
        exc_info=(type(exc), exc, exc.__traceback__),
    )

    from rest_framework.response import Response
    from rest_framework import status

    return Response(
        {
            "status": 0,
            "message": "An unexpected error occurred.",
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )