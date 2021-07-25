import os
import sys
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './service_account.json'


def create_bucket_class_location():
    """create new bucket in specific location with storage class"""

    # initialize client
    storage_client = storage.Client()
    
    # input the bucket name
    bucket = storage_client.bucket(bucket_name)

    # set storage class, by default STANDARD
    bucket.storage_class = "COLDLINE"

    # create new bucket
    new_bucket = storage_client.create_bucket(bucket, location='us-central1')

    # print new bucket detail
    print(vars(bucket))

    return new_bucket


def get_list_of_buckets():
    """get list of buckets"""

    # initialize client
    storage_client = storage.Client()

    # get list of buckets
    buckets = storage_client.list_buckets()

    list_of_buckets = []
    for bucket in buckets:
        list_of_buckets.append(bucket.name)

    return list_of_buckets


def get_specific_bucket():
    """get single bucket"""

    # initialize client
    storage_client = storage.Client()

    # retrieve a bucket
    bucket = storage_client.get_bucket(bucket_name)

    return bucket

def upload_to_bucket(bucket_name, path_to_source_file, upload_file_name):
    """upload file to bucket"""

    try:
        # initialize client
        storage_client = storage.Client()

        # input bucket name
        bucket = storage_client.bucket(bucket_name)

        # set the upload file name
        blob = bucket.blob(upload_file_name)

        # set the path to source file
        blob.upload_from_filename(path_to_source_file)
    
    except Exception as err:
        raise err
        sys.exit(1)

    return None


def download_file_from_bucket(bucket_name, path_to_storage_file_name, download_file_name):
    try:
        # initialize client
        storage_client = storage.Client()

        # input bucket name
        bucket = storage_client.bucket(bucket_name)

        # set the storage object name
        blob = bucket.blob(path_to_storage_file_name)

        # set the path to source file
        blob.download_to_filename(download_file_name)
    
    except Exception as err:
        raise err
        sys.exit(1)

    return None


bucket_name = 'agi_data_bucket'
src_file_name = './src/ready_to_upload.txt'

# create_bucket_class_location(bucket_name)
# print(get_list_of_buckets())
# get_specific_bucket(bucket_name)
# upload_to_bucket(bucket_name, src_file_name, 'src/dummy_text.txt')
# download_file_from_bucket(bucket_name, 'src/dummy_text.txt', './src/download_text.txt')