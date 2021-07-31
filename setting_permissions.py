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

    # reference: 
    # - https://cloud.google.com/storage/docs/access-control/iam-roles
    # - https://googleapis.dev/python/storage/latest/buckets.html
    policy.bindings.append({"role": role, "members": {f"user:{member}"}})

    bucket.set_iam_policy(policy)

    print("Added {} with role {} to {}.".format(member, role, bucket_name))


def set_access_control_list_object(bucket_name, object_name, user_email, permission='read'):
    """to set permissions in object level"""

    # initialize client
    storage_client = storage.Client()

    # input the bucket name
    bucket = storage_client.bucket(bucket_name)

    # input the object name
    blob = bucket.blob(object_name)

    # Reload fetches the current ACL from Cloud Storage
    blob.acl.reload()

    # can use `group`, `domain`, `all_authenticated` and `all` to grant access to different types of entities
    # can also use `grant_read` or `grant_write` to grant different roles
    if permission == 'own':
        blob.acl.user(user_email).grant_owner()
    elif permission == 'read':
        blob.acl.user(user_email).grant_read()

    blob.acl.save()

    print(
        "added user {} to '{}' on object {} in bucket {}.".format(
            user_email, permission, object_name, bucket_name
        )
    )


bucket_name = 'agi_dummy_bucket'
user_email = 'ragindaf22@gmail.com'
obj_name = 'download_img.jpg'

set_iam_permission_bucket(bucket_name, 'roles/storage.objectAdmin', user_email)
# set_access_control_list_object(bucket_name, obj_name, user_email)