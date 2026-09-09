from .models import Invitation
import re

def create_token(created_by, role):
    invitation = Invitation.objects.create(
        role=role,
        created_by=created_by
    )
    return invitation


def validate_ghana_card(number):
    pattern = r'^GHA-[0-9]{9}-[0-9]'
    if re.match(pattern, number):
        return True
    return False
