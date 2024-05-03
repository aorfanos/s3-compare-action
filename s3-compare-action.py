#################################################
# Read files from a remote S3-compatible bucket #
# and compare them to a given local directory   #
#################################################

# ref: https://developers.cloudflare.com/r2/examples/aws/boto3

import boto3
import json
import os

# inputs
access_key_id = os.environ.get("INPUT_ACCESS_KEY_ID")
bucket_name = os.environ.get("INPUT_BUCKET_NAME")
bucket_endpoint = os.environ.get("INPUT_BUCKET_ENDPOINT")
bucket_path = os.environ.get("INPUT_BUCKET_PATH")  # leave empty for /
local_path = os.environ.get("INPUT_LOCAL_PATH")
max_keys = os.environ.get("INPUT_MAX_KEYS", 50)
region = os.environ.get(
    "INPUT_REGION"
)  # Must be one of: wnam, enam, weur, eeur, apac, auto
secret_access_key = os.environ.get("INPUT_SECRET_ACCESS_KEY")

# create a set to store bucket contents/filenames
BucketContents = set()

# create another set to store local directory contents/filenames
LocalContents = set()

# connect to s3
s3 = boto3.client(
    service_name="s3",
    endpoint_url=bucket_endpoint,
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    region_name=region,
)

# read bucket contents
# ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_objects_v2.html
object_information = s3.list_objects_v2(
    Bucket=str(bucket_name), Prefix=bucket_path, Delimiter="/", MaxKeys=int(max_keys)
)

# get bucket file names
for key, val in object_information.items():
    if key == "Contents":
        for file in val:
            BucketContents.add(file["Key"])

# get local file names
local_files = os.listdir(local_path)

for file in local_files:
    LocalContents.add(file)

diff = BucketContents.difference(LocalContents)

# set GH output to differences list
os.environ["GITHUB_OUTPUT"] = json.dumps(list(diff))
