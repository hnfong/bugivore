from djangodev.contrib.messages.api import get_messages


def messages(request):
    """
    Returns a lazy 'messages' context variable.
    """
    return {'messages': get_messages(request)}
