"""
Error handling utilities for the application.
"""

import logging
from typing import Dict, Any, Tuple
from flask import Flask, jsonify

logger = logging.getLogger(__name__)


class APIError(Exception):
    """Custom API error with status code."""

    def __init__(self, message: str, status_code: int = 400, payload: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary."""
        result = {'error': self.message, **self.payload}
        return result


def register_error_handlers(app: Flask) -> None:
    """Register error handlers with Flask app."""

    @app.errorhandler(APIError)
    def handle_api_error(error: APIError):
        """Handle custom API errors."""
        logger.warning(f"API Error {error.status_code}: {error.message}")
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(400)
    def handle_bad_request(error):
        """Handle bad request errors."""
        logger.warning(f"Bad Request: {error}")
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle not found errors."""
        logger.warning(f"Not Found: {error}")
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Handle method not allowed errors."""
        logger.warning(f"Method Not Allowed: {error}")
        return jsonify({'error': 'Method not allowed'}), 405

    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle internal server errors."""
        logger.exception("Internal Server Error")
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Handle unexpected errors."""
        logger.exception(f"Unexpected error: {error}")
        return jsonify({'error': 'An unexpected error occurred'}), 500
