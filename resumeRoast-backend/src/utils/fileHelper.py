import os
import aiofiles


# Note : All PDF , image , wordDocs , video are stored in bytes
async def save_to_disk(file_bytes: bytes, file_path: str) -> bool:
    # Create all necessary directories in the file path
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Open a file to save data in binary mode ('wb' = write-binary)
    # 'async with' → Open the file, use it, and close it automatically when done
    async with aiofiles.open(file_path, "wb") as opened_file:
        # Write the file content (in bytes), and wait until writing is complete
        await opened_file.write(file_bytes)

    return True
