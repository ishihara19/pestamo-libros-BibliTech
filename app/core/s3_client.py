import boto3
from botocore.client import Config

class S3Client:
    """Cliente para interactuar con un servicio S3 compatible (como AWS S3 o Cloudflare R2)."""
    def __init__(self, endpoint_url: str, access_key_id: str, secret_access_key: str, bucket_name: str, domain: str):
        self.client = boto3.client(
            "s3",
            region_name="auto",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            config=Config(signature_version="s3v4"),
        )
        self.bucket_name = bucket_name
        self.domain = domain

    def upload_fileobj(self, file_obj, file_key: str, content_type: str):
        """Sube un objeto de archivo al bucket S3."""
        self.client.upload_fileobj(
            file_obj,
            self.bucket_name,
            file_key,
            ExtraArgs={"ContentType": content_type}
        )

    def generate_file_url(self, file_key: str) -> str:
        """Genera la URL pública para un archivo en el bucket S3."""
        return f"https://{self.domain}/{file_key}"