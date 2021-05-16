from oat.models.db.base_model import BaseModel


class DatasetsModel(BaseModel):
    def __init__(self):
        super().__init__(db_endpoint="datasets")

    @property
    def default_headers(self):
        return ["name", "id", "info", "created_by", "collection_ids", "collaborator_ids"]