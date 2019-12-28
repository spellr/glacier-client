import base64
import dateutil.parser
from datetime import datetime
from xml.etree import ElementTree


class Archive:
    def __init__(self, archive_item):
        self.creation_date: datetime = dateutil.parser.parse(archive_item["CreationDate"])
        self.size: int = archive_item["Size"]
        self.hash: str = archive_item["SHA256TreeHash"]
        description = archive_item["ArchiveDescription"]
        self.path = base64.urlsafe_b64decode(ElementTree.fromstring(description).find('p').text).decode('utf8')
        self.is_dir: bool = self.path.endswith('/')

    def __repr__(self):
        return f"Archive(path={self.path}, size={self.size})"
