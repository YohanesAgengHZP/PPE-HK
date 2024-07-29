from pydantic import BaseModel


class Base64File(BaseModel):
    filename: str
    file_base64: str
