from .models import Invitation


def create_token(created_by, role):
    invitation = Invitation.objects.create(
        role=role,
        created_by=created_by
    )
    return invitation