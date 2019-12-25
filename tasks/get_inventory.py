import boto3

from regions import Region
from tasks.base_task import Task
from keys import PUBLIC_KEY, SECRET_KEY


class GetInventoryTask(Task):
    def __init__(self, region: Region, vault: str):
        super(GetInventoryTask, self).__init__()
        self.region = region
        self.vault = vault

    def run(self):
        session = boto3.session.Session()
        client = session.client('glacier', region_name=self.region.code,
                                aws_access_key_id=PUBLIC_KEY, aws_secret_access_key=SECRET_KEY)
        job = client.initiate_job(vaultName=self.vault, jobParameters={"Type": "inventory-retrieval"})
        print(job["jobId"])

    def __repr__(self):
        return f"Getting last inventory from region '{self.region.name}', vault '{self.vault}'"
