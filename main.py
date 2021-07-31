import os
import sys
from google.cloud import storage
from init_client import create_client

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './service_account.json'


def create_bucket(bucket_name):
    """create new bucket in specific location with storage class"""

    # initialize client & get bucket
    storage_client, bucket, _ = create_client(bucket_name)

    # set storage class, by default STANDARD
    bucket.storage_class = "COLDLINE"

    # create new bucket
    new_bucket = storage_client.create_bucket(bucket, location='us-central1')

    # print new bucket detail
    print(vars(bucket))

    return None


def get_specific_bucket(bucket_name):
    """get a single bucket"""

    # initialize client & get bucket
    _, bucket, _ = create_client(bucket_name)

    return bucket


def get_list_of_buckets():
    """get list of all buckets"""

    # initialize client
    storage_client = storage.Client()

    # get list of buckets
    buckets = storage_client.list_buckets()

    list_of_buckets = []
    for bucket in buckets:
        list_of_buckets.append(bucket.name)

    return list_of_buckets


def upload_to_bucket(bucket_name, path_to_source_file, upload_file_name):
    """upload file to bucket"""

    try:
        # initialize client & get blob
        _, _, blob = create_client(bucket_name, upload_file_name)

        # set the path to source file
        blob.upload_from_filename(path_to_source_file)
    
    except Exception as err:
        raise err
        sys.exit(1)
    
    else:
        print(f"upload file '{path_to_source_file}' succeed")

    return None


def download_specific_object(bucket_name, path_to_storage_file_name, download_file_name):
    """download specific object from bucket"""

    try:
        # initialize client & get blob
        _, _, blob = create_client(bucket_name, path_to_storage_file_name)

        # set the path to source file
        blob.download_to_filename(download_file_name)
    
    except Exception as err:
        raise err
        sys.exit(1)
    
    else:
        print(f"download object '{path_to_storage_file_name}' succeed")

    return None


def get_list_of_objects(bucket_name, prefix=None, delimiter=None):
    """get lists of all the objects in the bucket"""

    # initialize client
    storage_client = storage.Client()

    # get list objects
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix, delimiter=delimiter)

    for blob in blobs:
        print(blob.name)

    if delimiter:
        print("Prefixes:")
        for prefix in blobs.prefixes:
            print(prefix)

    return None


def copy_object(bucket_name, blob_name, destination_bucket_name, destination_blob_name):
    """copies an object from one bucket to another with a new name"""

    # initialize client, get bucket, & get blob
    storage_client, source_bucket, source_blob = create_client(bucket_name, blob_name)

    # set destination bucket name
    destination_bucket = storage_client.bucket(destination_bucket_name)

    # copy object
    blob_copy = source_bucket.copy_blob(
        source_blob, destination_bucket, destination_blob_name
    )

    print(
        "object {} in bucket {} copied to blob {} in bucket {}.".format(
            source_blob.name,
            source_bucket.name,
            blob_copy.name,
            destination_bucket.name,
        )
    )


def delete_object(bucket_name, blob_name):
    """delete an object from the bucket"""

    # initialize client, get bucket, & get blob
    _, _, blob = create_client(bucket_name, blob_name)

    # delete object
    blob.delete()

    print("object {} deleted".format(blob_name))


bucket_name = 'agi_dummy_bucket'
src_file_name1 = './src/ready_to_upload_txt.txt'
src_file_name2 = './src/ready_to_upload_txt2.txt'
src_file_name3 = './src/ready_to_upload_img.jpg'
src_file_name4 = './src/ready_to_upload_img2.jpg'

# create_bucket(bucket_name)

# print(get_specific_bucket(bucket_name))
# print(get_list_of_buckets())

# upload_to_bucket(bucket_name, src_file_name1, 'src/download_txt.txt')
# upload_to_bucket(bucket_name, src_file_name2, 'src/download_txt2.txt')
# upload_to_bucket(bucket_name, src_file_name2, 'src/src2/download_txt2.txt')
# upload_to_bucket(bucket_name, src_file_name3, 'download_img.jpg')
# upload_to_bucket(bucket_name, src_file_name4, 'download_img2.jpg')

# download_specific_object(bucket_name, 'download_img2.jpg', './src/download_img.jpg')

# get_list_of_objects(bucket_name)
# get_list_of_objects(bucket_name, 'src/', '/')

# copy_object(bucket_name, 'download_img.jpg', bucket_name, 'src/src2/copied_img.jpg')

# delete_object(bucket_name, 'src/src2/copied_img.jpg')