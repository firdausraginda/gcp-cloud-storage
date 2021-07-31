import os
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './service_account.json'

def create_client(bucket_name, object_name=None):

    # initialize client
    storage_client = storage.Client()

    # input the bucket name
    bucket = storage_client.bucket(bucket_name)

    # input the object name
    if object_name:
        blob = bucket.blob(object_name)
    else:
        blob = None

    return storage_client, bucket, blob