import os
from google.cloud import storage
from init_client import create_client
from set_role_and_member_permissions import get_member_bucket_level, get_role_bucket_level, get_member_blob_level, grant_role_blob_level, revoke_role_blob_level


def set_iam_permission_bucket(bucket_name, role_type, member_type):
    """to set permissions in bucket level"""

    # initialize client & get bucket
    _, bucket, _ = create_client(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)

    # get member type
    member_value = get_member_bucket_level(member_type)

    # get role type
    role_value = get_role_bucket_level(role_type)

    # set role(s) to member(s)
    policy.bindings.append({"role": role_value, "members": {member_value}})

    bucket.set_iam_policy(policy)

    print("added {} with role {} to {}".format(member_value, role_value, bucket_name))


def remove_permission_from_bucket(bucket_name, role_type, member_type):
    """remove member from bucket"""

    # initialize client & get bucket
    _, bucket, _ = create_client(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)
    
    # get member type
    member_value = get_member_bucket_level(member_type)

    # get role type
    role_value = get_role_bucket_level(role_type)

    for binding in policy.bindings:
        # print(binding)
        if binding["role"] == role_value and binding.get("condition") is None:
            # revoke role from member
            binding["members"].discard(member_value)

    bucket.set_iam_policy(policy)

    print("removed {} with role {} from {}".format(member_value, role_value, bucket_name))


def set_access_control_list_blob(bucket_name, blob_name, role_type, member_type):
    """to set permissions in blob level"""

    # initialize client, get bucket, & get blob
    _, _, blob = create_client(bucket_name, blob_name)

    # reload fetches the current ACL from cloud storage
    blob.acl.reload()

    # get member type
    member = get_member_blob_level(member_type, blob)
    
    # grant role to member
    grant_role_blob_level(role_type, member)

    blob.acl.save()

    print(
        "added {} to '{}' on blob {} in bucket {}".format(
            member_type, role_type, blob_name, bucket_name
        )
    )


def remove_permission_from_blob(bucket_name, blob_name, role_type, member_type):
    """remove member from access control list of an blob"""

    # initialize client, get bucket, & get blob
    _, _, blob = create_client(bucket_name, blob_name)
    
    # get member type
    member = get_member_blob_level(member_type, blob)
        
    # revoke role from member
    revoke_role_blob_level(role_type, member)

    blob.acl.save()

    print(
        "removed permission for {} to {} from blob {} in bucket {}".format(
            member_type, role_type, blob_name, bucket_name
        )
    )

bucket_name = 'agi_dummy_bucket'
user_email = 'ragindaF22@gmail.com'
obj_name = 'src/src2/download_txt2.txt'


# set_iam_permission_bucket(bucket_name, 'own', user_email)
# set_iam_permission_bucket(bucket_name, 'own', 'auth_public')
# set_iam_permission_bucket(bucket_name, 'own', 'public')

# remove_permission_from_bucket(bucket_name, 'own', user_email)
# remove_permission_from_bucket(bucket_name, 'own', 'auth_public')
# remove_permission_from_bucket(bucket_name, 'own', 'public')

# set_access_control_list_blob(bucket_name, obj_name, 'own', user_email)
# set_access_control_list_blob(bucket_name, obj_name, 'own', 'public')
# set_access_control_list_blob(bucket_name, obj_name, 'own', 'auth_public')

# remove_permission_from_blob(bucket_name, obj_name, 'own', user_email)
# remove_permission_from_blob(bucket_name, obj_name, 'own', 'public')
# remove_permission_from_blob(bucket_name, obj_name, 'own', 'auth_public')