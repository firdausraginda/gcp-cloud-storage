import os
from google.cloud import storage
from init_client import create_client
from set_role_and_member_permissions import *

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './service_account.json'


def set_iam_permission_bucket(bucket_name, role, member):
    """to set permissions in bucket level"""

    # initialize client & get bucket name
    _, bucket, _ = create_client(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)

    # get member
    member_set = get_member_bucket_level(member)

    # get role
    role_set = get_role_bucket_level(role)

    # grant role to member
    policy.bindings.append({"role": role_set, "members": {member_set}})

    bucket.set_iam_policy(policy)

    print("added {} with role {} to {}".format(member, role, bucket_name))


def remove_permission_from_bucket(bucket_name, role, member):
    """remove member from bucket"""

    # initialize client & get bucket name
    _, bucket, _ = create_client(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)
    
    # get member
    member_set = get_member_bucket_level(member)

    # get role
    role_set = get_role_bucket_level(role)

    for binding in policy.bindings:
        # print(binding)
        if binding["role"] == role_set and binding.get("condition") is None:
            # revoke role from member
            binding["members"].discard(member_set)

    bucket.set_iam_policy(policy)

    print("removed {} with role {} from {}".format(member, role, bucket_name))


def set_access_control_list_object(bucket_name, object_name, role, member):
    """to set permissions in object level"""

    # initialize client, get bucket, & get blob
    _, bucket, blob = create_client(bucket_name, object_name)

    # Reload fetches the current ACL from Cloud Storage
    blob.acl.reload()

    # get member
    member_set = get_member_object_level(member, blob)
    
    # grant role to member
    grant_role_object_level(role, member_set)

    blob.acl.save()

    print(
        "added user {} to '{}' on object {} in bucket {}".format(
            member, role, object_name, bucket_name
        )
    )


def remove_permission_from_object(bucket_name, object_name, role, member):
    """remove member from access control list of an object"""

    # initialize client, get bucket, & get blob
    _, bucket, blob = create_client(bucket_name, object_name)
    
    # get member
    member_set = get_member_object_level(member, blob)
        
    # revoke role from member
    revoke_role_object_level(role, member_set)

    blob.acl.save()

    print(
        "removed permission for {} to {} from object {} in bucket {}".format(
            member, role, object_name, bucket_name
        )
    )

bucket_name = 'agi_dummy_bucket'
user_email = 'ragindaF22@gmail.com'
obj_name = 'src/copied_img.jpg'

# set_iam_permission_bucket(bucket_name, 'own', user_email)
# set_iam_permission_bucket(bucket_name, 'own', 'auth_public')
# set_iam_permission_bucket(bucket_name, 'own', 'public')

# remove_permission_from_bucket(bucket_name, 'own', user_email)
# remove_permission_from_bucket(bucket_name, 'own', 'auth_public')
# remove_permission_from_bucket(bucket_name, 'own', 'public')

# set_access_control_list_object(bucket_name, obj_name, 'own', user_email)
# set_access_control_list_object(bucket_name, obj_name, 'own', 'public')
# set_access_control_list_object(bucket_name, obj_name, 'own', 'auth_public')

# remove_permission_from_object(bucket_name, obj_name, 'own', user_email)
# remove_permission_from_object(bucket_name, obj_name, 'own', 'public')
# remove_permission_from_object(bucket_name, obj_name, 'own', 'auth_public')