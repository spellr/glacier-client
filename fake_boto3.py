from unittest.mock import MagicMock

boto3 = MagicMock()
client = boto3.session.Session.return_value.client.return_value

client.list_vaults.return_value = {
    "VaultList": [
        {
            "VaultName": "vault"
        }
    ]
}

client.describe_job.return_value = {
    "Completed": True
}

client.get_job_output.return_value = {
    "body": open('inventory.json')
}
