import json
from django.contrib.messages import get_messages


def toast_messages(request):
    messages = get_messages(request)
    serialized = [
        {'text': str(message), 'tags': message.tags}
        for message in messages
    ]
    return {
        'toast_messages_json': json.dumps(serialized)
    }