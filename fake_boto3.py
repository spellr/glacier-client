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


def get_inventory(vaultName, jobId):
    return {
        "body": open('inventory.json', 'rb')
    }


client.get_job_output.side_effect = get_inventory
