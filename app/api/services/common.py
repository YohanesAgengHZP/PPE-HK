import aiofiles
import binascii
import os

from base64 import b64decode
from fastapi import HTTPException

from core.settings import STATIC_ROOT


async def save_file(file_base64: str, filename: str, dir_path: str) -> None:
    """
    Decode base64 file and save to static folder.

    Args:
        file_base64 (str): Base64 representation of the file.
        filename (str): Filename.
        dir_path (str): Directory path relative to the static folder.

    Raises:
        HTTPException: 400 Error while decoding the base64 string.
        HTTPException: 500 Error while uploading the file.
    """

    try:
        file_content = b64decode(file_base64.encode("utf-8"))
        folder_path = os.path.join(STATIC_ROOT, dir_path)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        filepath = os.path.join(folder_path, filename)
        async with aiofiles.open(filepath, "wb") as out_file:
            await out_file.write(file_content)
    except binascii.Error:
        raise HTTPException(
            status_code=400,
            detail="There was an error decoding the base64 string",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="There was an error uploading the file",
        )


async def delete_file(filename: str, dir_path: str) -> None:
    """
    Delete a file from static folder.

    Args:
        filename (str): Filename.
        dir_path (str): Directory path relative to the static folder.

    Raises:
        HTTPException: 500 Error while deleting the file.
    """

    try:
        file_path = os.path.join(STATIC_ROOT, dir_path, filename)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="There was an error deleting the file",
        )
