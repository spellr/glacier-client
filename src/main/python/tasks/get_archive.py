import logging

from archive import Archive
from regions import Region
from task_manager import TaskManager
from tasks.base_task import Task
from tasks.wait_for_job import WaitForJobTask, JobOutput


class GetArchiveTask(Task):
    def __init__(self, region: Region, vault: str, archive: Archive, output_file: str):
        super(GetArchiveTask, self).__init__(region)
        self.archive: Archive = archive
        self.vault = vault
        self.output_file = output_file

    def __repr__(self):
        return f"Requesting archive {self.archive.description} from region '{self.region.name}', vault '{self.vault}'"

    def run(self):
        client = self.get_boto_client()
        logging.info("Initiating job to retrieve archive")
        job_params = {
            "Type": "archive-retrieval",
            "ArchiveId": self.archive.id,
            "Tier": "Bulk"
        }
        job = client.initiate_job(vaultName=self.vault, jobParameters=job_params)
        logging.info(f"Initiated job to retrieve archive. Job id = {job['jobId']}")

        TaskManager.add_task(WaitForJobTask(self.region, self.vault, job, JobOutput.ARCHIVE, self.output_file))
