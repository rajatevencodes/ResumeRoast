# rag/worker.py
from bson import ObjectId
from models.files import files_collection, FileStatus
from rag.main import app


async def perform_rag_with_worker(file_id: str, filename: str):
    """
    Main worker function that now receives the filename.
    """
    try:
        # ✅ Reconstruct the path using both arguments
        file_path = f"/mnt/uploads/{file_id}/{filename}"

        initial_state = {
            "file_id": file_id,
            "file_path": file_path,
        }

        await app.ainvoke(initial_state)

    except Exception as e:
        print(f"Error processing file {file_id}: {e}")
        await files_collection.update_one(
            {"_id": ObjectId(file_id)},
            {"$set": {"status": FileStatus.FAILED, "result": str(e)}},
        )
