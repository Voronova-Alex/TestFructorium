import json
import logging
import threading
import uuid

from django.core.handlers.wsgi import WSGIRequest
from rest_framework.response import Response

logger = logging.getLogger("custom_django_request")
local_storage = threading.local()


class RequestIDFilter(logging.Filter):
    """Фильтр добавляющий request_id запроса."""

    def filter(self, record) -> bool:
        default_request_id = "unknown"
        record.request_id = getattr(local_storage, "request_id", default_request_id)
        return True


class LoggingMiddleware:
    """Логирование запросов с расширенной информацией."""

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: WSGIRequest) -> Response:
        # Code that is executed in each request before the view is called
        request = self.before_view(request)

        response = self.get_response(request)

        # Code that is executed in each request after the view is called
        self.after_view(request, response)

        return response

    def before_view(self, request: WSGIRequest) -> WSGIRequest:
        """Обработка запроса перед view."""
        local_storage.request_id = uuid.uuid4().hex
        return request

    @staticmethod
    def get_request_body(request):
        return "-"

    def after_view(self, request: WSGIRequest, response: Response) -> None:
        """Обработка запроса после view."""
        response_body = getattr(response, "data", None)
        status_code = getattr(response, "status_code", None)

        msg = (
            f"[{request.method} {request.get_full_path()} {status_code}] "
            f"[user: {request.user}]"
        )

        if 200 <= status_code < 400:
            logger.info(msg)
        else:
            request_body = self.get_request_body(request)
            if 400 <= status_code < 500:
                request_msg = f" [request: {request_body}] [response: {response_body}]"
                logger.warning(" ".join((msg, request_msg)))
            else:
                request_msg = f" [request: {request_body}] [response: {response_body}]"
                logger.error(" ".join((msg, request_msg)))
