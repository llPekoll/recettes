from b2sdk.v2 import B2Api, InMemoryAccountInfo
import tempfile
from elisasrecipe import settings


info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account(
    "production", settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY
)


def upload_image_to_b2(img, image_type: str) -> str:
    """

    local_file_path: location of the file in the containter -> use temporary file
    b2_file_name: location of the file in the bukcet
    """
    tmp = tempfile.NamedTemporaryFile()
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(img)
        print(tmp)
    local_file_path = tmp.name
    b2_file_name = f"{settings.PRODUCTION_STATE}/{image_type}/{img}"
    bucket = b2_api.get_bucket_by_name(settings.AWS_STORAGE_BUCKET_NAME)
    file_info = {
        "production_state": settings.PRODUCTION_STATE,
    }
    bucket.upload_local_file(
        local_file=local_file_path,
        file_name=b2_file_name,
        file_infos=file_info,
    )
    return f"{settings.AWS_S3_ENDPOINT_URL}/{b2_file_name}"
