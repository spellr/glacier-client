import base64
import dateutil.parser
from datetime import datetime
from xml.etree import ElementTree


class Archive:
    def __init__(self, archive_item):
        self.creation_date: datetime = dateutil.parser.parse(archive_item["CreationDate"])
        self.size: int = archive_item["Size"]
        self.hash: str = archive_item["SHA256TreeHash"]
        self.description = archive_item["ArchiveDescription"]

    def __repr__(self):
        return f"Archive(description={self.description}, size={self.size})"
