import os
import logging

from treehash import TreeHash

from consts import UPLOAD_PART_SIZE
from regions import Region
from tasks.base_task import Task


class UploadFileTask(Task):
    def __init__(self, region: Region, vault: str, file_location: str):
        super(UploadFileTask, self).__init__(region)
        self.vault = vault
        self.file_location = file_location
        self.file_name = os.path.basename(file_location)
        self.file_size = os.path.getsize(self.file_location)
        self.cur_part = 0
        self.numof_parts = int((self.file_size - 1) / UPLOAD_PART_SIZE) + 1

    def run(self):
        client = self.get_boto_client()
        logging.info("Initiating job to upload")
        upload_job = client.initiate_multipart_upload(vaultName=self.vault, archiveDescription=self.file_name,
                                                      partSize=str(UPLOAD_PART_SIZE))
        upload_id = upload_job['uploadId']

        treehash = TreeHash(block_size=1024**2)

        cur_file = open(self.file_location, 'rb')

        i = 0
        for i in range(self.numof_parts-1):
            self.cur_part += 1
            self.update_task()

            data = cur_file.read(UPLOAD_PART_SIZE)
            treehash.update(data)

            cur_range = 'bytes %d-%d/*' % (i*UPLOAD_PART_SIZE, (i+1)*UPLOAD_PART_SIZE-1)
            client.upload_multipart_part(vaultName=self.vault, uploadId=upload_id, range=cur_range, body=data)

        self.cur_part += 1
        self.update_task()

        data = cur_file.read(UPLOAD_PART_SIZE)
        treehash.update(data)

        cur_range = 'bytes %d-%d/*' % (i * UPLOAD_PART_SIZE, self.file_size-1)
        client.upload_multipart_part(vaultName=self.vault, uploadId=upload_id, range=cur_range, body=data)

        cur_file.close()

        hash_res = treehash.hexdigest()
        client.complete_multipart_upload(vaultName=self.vault, uploadId=upload_id,
                                         archiveSize=str(self.file_size), checksum=hash_res)

    def __repr__(self):
        return f"Initiating upload of file '{self.file_name}' to vault '{self.vault}' in region '{self.region.name}'" \
               f" (Part {self.cur_part}/{self.numof_parts})"
