def get_member_bucket_level(member_type):
    """get member type permissions on bucket level"""

    # set member type
    if member_type == 'public':
        member_value = 'allUsers'
    elif member_type == 'auth_public':
        member_value = 'allAuthenticatedUsers'
    else:
        member_value = f'user:{member_type}'

    return member_value


def get_role_bucket_level(role_type):
    """get role type permissions on bucket level"""

    # set role type
    if role_type == 'own':
        role_value = 'roles/storage.objectAdmin'
    elif role_type == 'write':
        role_value = 'roles/storage.objectCreator'
    elif role_type == 'read':
        role_value = 'roles/storage.objectViewer'

    return role_value


def get_member_blob_level(member_type, blob):
    """get member type permissions on blob level"""

    # set member
    if member_type == 'public':
        member = blob.acl.all()
    elif member_type == 'auth_public':
        member = blob.acl.all_authenticated()
    else:
        member = blob.acl.user(member_type)
    
    return member


def grant_role_blob_level(role_type, member):
    """grant a role permission on blob level"""

    if role_type == 'own':
        member.grant_owner()
    elif role_type == 'read':
        member.grant_read()

    return None


def revoke_role_blob_level(role_type, member):
    """revoke a role permission on blob level"""

    if role_type == 'own':
        member.revoke_owner()
    elif role_type == 'read':
        member.revoke_read()

    return None