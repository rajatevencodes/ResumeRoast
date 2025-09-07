from enum import Enum

from typing import Optional

from pydantic import BaseModel, Field
from pymongo.asynchronous.collection import AsyncCollection
from db.connectDB import db


class FileStatus(str, Enum):
    PENDING = "pending"
    QUEUED = "Wait... Your file is in the queue"
    PROCESSING = "processing"
    CONVERTING_TO_IMAGE = "Converting your PDF to Images"
    ENCODING_IMAGE = "Converting Image to Readable Format"
    ROASTING_WITH_AI = "Generating roast with AI ..."
    COMPLETED = "Ready to be Roasted ? 🙃"
    FAILED = "Processing Failed ❌"


class FileModel(BaseModel):
    """
    Represents a file record in the database.
    """

    # Default _id is already there :)

    name: str = Field(..., description="The original name of the uploaded file")

    status: FileStatus = Field(
        default=FileStatus.PENDING, description="The processing status of the file"
    )

    ai_response: Optional[str] = Field(
        None, description="The result from the AI analysis"
    )


COLLECTION_NAME = "files"
files_collection: AsyncCollection = db[COLLECTION_NAME]
