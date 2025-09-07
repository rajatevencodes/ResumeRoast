from fastapi import UploadFile, FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from utils.fileHelper import save_to_disk
from db.connectDB import test_connection
from models.files import FileModel, files_collection, FileStatus
from task_queue.q import queue
from task_queue.worker import perform_rag_with_worker
from bson import ObjectId
from fastapi import Path

app = FastAPI(title="Resume Roaster 😈", description="Roast Resume without mercy")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Type"],
)


@app.get("/healthcheck")
def read_root():
    return {"message": "🎉 App is working ☺️👌"}


@app.post("/upload")
async def upload_file(file: UploadFile):
    try:
        # Test MongoDB connection
        await test_connection()

        file_to_insert = FileModel(name=file.filename)

        # As we are using BaseModel, we can use model_dump to convert it to a dict
        uploaded_file = await files_collection.insert_one(file_to_insert.model_dump())

        file_path = f"/mnt/uploads/{str(uploaded_file.inserted_id)}/{file.filename}"  # inserted_id - ObjectId from MongoDB

        # Save file to disk asynchronously
        await save_to_disk(await file.read(), file_path)

        # Push file to queue
        queue.enqueue(
            perform_rag_with_worker, str(uploaded_file.inserted_id), file.filename
        )

        # Update the Status to QUEUED
        await files_collection.update_one(
            {"_id": uploaded_file.inserted_id},
            {"$set": {"status": FileStatus.QUEUED}},
        )

        return {"file_id": str(uploaded_file.inserted_id)}

    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return {"error": str(e)}


@app.get("/{id}")
async def get_file_by_id(id: str = Path(..., description="ID of the file")):
    db_file = await files_collection.find_one({"_id": ObjectId(id)})

    # TODO : Debug - Remove it
    print(db_file)

    return {
        "_id": str(db_file["_id"]),
        "name": db_file["name"],
        "status": db_file["status"],
        "ai_response": db_file["ai_response"] if "ai_response" in db_file else None,
    }


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
