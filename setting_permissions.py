import os
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './service_account.json'


def set_iam_permission_bucket(bucket_name, role, member):
    """to set permissions in bucket level"""

    # initialize client
    storage_client = storage.Client()

    # input the bucket name
    bucket = storage_client.bucket(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)
    
    # set role
    if role == 'own':
        role_set = 'roles/storage.objectAdmin'
    elif role == 'write':
        role_set = 'roles/storage.objectCreator'
    elif role == 'read':
        role_set = 'roles/storage.objectViewer'

    # set member
    if member == 'public':
        member_set = {f"allUsers"}
    elif member == 'auth_public':
        member_set = {f"allAuthenticatedUsers"}
    else:
        member_set = {f"user:{member}"}

    policy.bindings.append({"role": role_set, "members": member_set})

    bucket.set_iam_policy(policy)

    print("added {} with role {} to {}".format(member, role, bucket_name))


def remove_permission_from_bucket(bucket_name, role, member):
    """remove member from bucket"""

    # initialize client
    storage_client = storage.Client()

    # input the bucket name
    bucket = storage_client.bucket(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)
    
    # set role
    if role == 'own':
        role_set = 'roles/storage.objectAdmin'
    elif role == 'write':
        role_set = 'roles/storage.objectCreator'
    elif role == 'read':
        role_set = 'roles/storage.objectViewer'

    # set member
    if member == 'public':
        member_set = "allUsers"
    elif member == 'auth_public':
        member_set = "allAuthenticatedUsers"
    else:
        member_set = f"user:{member}"

    for binding in policy.bindings:
        # print(binding)
        if binding["role"] == role_set and binding.get("condition") is None:
            binding["members"].discard(member_set)

    bucket.set_iam_policy(policy)

    print("removed {} with role {} from {}".format(member, role, bucket_name))


def set_access_control_list_object(bucket_name, object_name, role, member):
    """to set permissions in object level"""

    # initialize client
    storage_client = storage.Client()

    # input the bucket name
    bucket = storage_client.bucket(bucket_name)

    # input the object name
    blob = bucket.blob(object_name)

    # Reload fetches the current ACL from Cloud Storage
    blob.acl.reload()

    # set member
    if member == 'public':
        member_set = blob.acl.all()
    elif member == 'auth_public':
        member_set = blob.acl.all_authenticated()
    else:
        member_set = blob.acl.user(member)
    
    # set role
    if role == 'own':
        member_set.grant_owner()
    elif role == 'read':
        member_set.grant_read()

    blob.acl.save()

    print(
        "added user {} to '{}' on object {} in bucket {}".format(
            member, role, object_name, bucket_name
        )
    )


def remove_permission_from_object(bucket_name, object_name, role, member):
    """remove member from access control list of an object"""

    # initialize client
    storage_client = storage.Client()

    # input the bucket name
    bucket = storage_client.bucket(bucket_name)

    # input the object name
    blob = bucket.blob(object_name)
    
    # set member
    if member == 'public':
        member_set = blob.acl.all()
    elif member == 'auth_public':
        member_set = blob.acl.all_authenticated()
    else:
        member_set = blob.acl.user(member)
        
    # set role
    if role == 'own':
        member_set.grant_owner()
    elif role == 'read':
        member_set.revoke_read()

    blob.acl.save()

    print(
        "removed permission for {} to {} from object {} in bucket {}".format(
            member, role, object_name, bucket_name
        )
    )

bucket_name = 'agi_dummy_bucket'
user_email = 'ragindaF22@gmail.com'
obj_name = 'src/copied_img.jpg'

# set_iam_permission_bucket(bucket_name, 'read', user_email)
# set_iam_permission_bucket(bucket_name, 'read', 'auth_public')
# set_iam_permission_bucket(bucket_name, 'read', 'public')

# remove_permission_from_bucket(bucket_name, 'read', user_email)
# remove_permission_from_bucket(bucket_name, 'read', 'auth_public')
# remove_permission_from_bucket(bucket_name, 'read', 'public')

# set_access_control_list_object(bucket_name, obj_name, 'read', user_email)
# set_access_control_list_object(bucket_name, obj_name, 'read', 'public')
# set_access_control_list_object(bucket_name, obj_name, 'read', 'auth_public')

# remove_permission_from_object(bucket_name, obj_name, 'read', user_email)
# remove_permission_from_object(bucket_name, obj_name, 'read', 'public')
# remove_permission_from_object(bucket_name, obj_name, 'read', 'auth_public')