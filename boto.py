import boto3

from consts import DEBUG
from regions import Region


def get_boto(region: Region, access_key: str = None, secret_key: str = None):
    endpoint_url = None
    if DEBUG:
        endpoint_url = "http://localhost:5000"

    session = boto3.session.Session()
    client = session.client('glacier', region_name=region.code, endpoint_url=endpoint_url,
                            aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    return client
