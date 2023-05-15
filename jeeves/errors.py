"""Errors used throughout."""

class InvalidInbound(Exception):
    """
    Raised when an inbound request is invalid, either because it's missing a required
    field or because the request is malformed.
    """


class ZapierAuthenticationError(Exception):
    """
    Raised when Zapier authentication fails, either on the side of checking access 
    token validity, refreshing access tokens, or onboarding a user initially.
    """
