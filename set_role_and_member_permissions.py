def get_member_bucket_level(member):
    """get member permissions on bucket level"""

    # set member
    if member == 'public':
        member_set = f"allUsers"
    elif member == 'auth_public':
        member_set = f"allAuthenticatedUsers"
    else:
        member_set = f"user:{member}"

    return member_set


def get_role_bucket_level(role):
    """get role permissions on bucket level"""

    # set role
    if role == 'own':
        role_set = 'roles/storage.objectAdmin'
    elif role == 'write':
        role_set = 'roles/storage.objectCreator'
    elif role == 'read':
        role_set = 'roles/storage.objectViewer'

    return role_set


def get_member_object_level(member, blob):
    """get member permissions on object level"""

    # set member
    if member == 'public':
        member_set = blob.acl.all()
    elif member == 'auth_public':
        member_set = blob.acl.all_authenticated()
    else:
        member_set = blob.acl.user(member)
    
    return member_set


def grant_role_object_level(role, member):
    """grant a role permission on object level"""

    # set role
    if role == 'own':
        member.grant_owner()
    elif role == 'read':
        member.grant_read()

    return None


def revoke_role_object_level(role, member):
    """revoke a role permission on object level"""

    # set role
    if role == 'own':
        member.revoke_owner()
    elif role == 'read':
        member.revoke_read()

    return None