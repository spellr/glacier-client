import uuid

import boto3

import consts


def setup_aws_mock():
    if not consts.DEBUG:
        return

    key = str(uuid.uuid4())

    session = boto3.session.Session()
    client = session.client('glacier', region_name="eu-west-3", endpoint_url='http://localhost:5000',
                            aws_access_key_id=key, aws_secret_access_key=key)

    client.create_vault(vaultName="speller")
    client.upload_archive(vaultName="speller", body=b"asdf", archiveDescription="archive.tar")
