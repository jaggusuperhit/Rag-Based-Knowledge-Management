from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError, ServiceRequestError
from config import Config

class AzureStorage:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(Config.AZURE_STORAGE_CONNECTION_STRING)
        self.container_client = self.blob_service_client.get_container_client(Config.AZURE_CONTAINER_NAME)

    def upload_file(self, file_obj, filename):
        try:
            blob_client = self.container_client.get_blob_client(filename)
            blob_client.upload_blob(file_obj)
            return True
        except ServiceRequestError as e:
            print(f"Error uploading file: {e}")
            return False

    def get_file(self, filename):
        try:
            blob_client = self.container_client.get_blob_client(filename)
            blob_data = blob_client.download_blob()
            return blob_data.content_as_bytes()
        except ResourceNotFoundError as e:
            print(f"File not found: {e}")
            return None
        except ServiceRequestError as e:
            print(f"Error retrieving file: {e}")
            return None