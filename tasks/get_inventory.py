import boto3

from consts import Region
from tasks.base_task import Task
from keys import PUBLIC_KEY, SECRET_KEY


class GetInventoryTask(Task):
    def __init__(self, region: Region):
        super(GetInventoryTask, self).__init__()
        self.region = region

    def run(self):
        session = boto3.session.Session()
        client = session.client('glacier', region_name=self.region.code,
                                aws_access_key_id=PUBLIC_KEY, aws_secret_access_key=SECRET_KEY)
        client.initiate_job()
