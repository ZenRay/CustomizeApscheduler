"""
Scheduler core exceptions
"""

# Basic Configurations
class NotConfigured(Exception):
    """Indicates a missing configuration situation"""
    pass


class NotSupported(Exception):
    """Indicates a feature or method is not supported"""
    pass


class NotSupportedArgument(Exception):
    """Indicates a argument is not supported"""
    pass