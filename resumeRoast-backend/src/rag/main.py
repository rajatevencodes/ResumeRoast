import os
import base64
import asyncio
from typing import TypedDict, List
from bson import ObjectId
from pdf2image import convert_from_path
from openai import OpenAI
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
from models.files import files_collection, FileStatus

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class GraphState(TypedDict):
    file_id: str
    file_path: str
    image_paths: List[str]
    images_base64: List[str]
    roast_result: str


async def start_processing_node(state: GraphState):
    """Sets the initial status to 'processing' in the database."""
    await files_collection.update_one(
        {"_id": ObjectId(state["file_id"])}, {"$set": {"status": FileStatus.PROCESSING}}
    )
    print(f"\n--- Status: Processing ---")
    return {}


async def convert_pdf_to_images_node(state: GraphState):
    """Converts the PDF to images using a non-blocking thread."""
    await files_collection.update_one(
        {"_id": ObjectId(state["file_id"])},
        {"$set": {"status": FileStatus.CONVERTING_TO_IMAGE}},
    )
    print(f"--- Status: Converting to Image ---")

    file_id = state["file_id"]
    file_path = state["file_path"]
    output_dir = os.path.join("/mnt/output_images", file_id)

    # Run blocking I/O in a separate thread
    await asyncio.to_thread(os.makedirs, output_dir, exist_ok=True)

    pages = await asyncio.to_thread(
        convert_from_path,
        file_path,
        output_folder=output_dir,
        fmt="jpeg",
        output_file=f"image-{file_id}",
    )
    image_paths = [page.filename for page in pages]
    print(f"Successfully converted PDF to {len(image_paths)} image(s).")
    return {"image_paths": image_paths}


async def encode_images_node(state: GraphState):
    """Encodes images to Base64 using a non-blocking thread."""
    await files_collection.update_one(
        {"_id": ObjectId(state["file_id"])},
        {"$set": {"status": FileStatus.ENCODING_IMAGE}},
    )
    print(f"--- Status: Encoding Images ---")

    def _encode_images():
        """Helper function to run in a thread."""
        encoded_list = []
        for img_path in state["image_paths"]:
            with open(img_path, "rb") as image_file:
                encoded_list.append(base64.b64encode(image_file.read()).decode("utf-8"))
        return encoded_list

    # Run blocking file reads in a separate thread
    images_base64 = await asyncio.to_thread(_encode_images)
    print(f"Successfully encoded {len(images_base64)} image(s).")
    return {"images_base64": images_base64}


async def call_openai_vision_node(state: GraphState):
    """Calls OpenAI Vision API with ALL pages of the resume."""
    await files_collection.update_one(
        {"_id": ObjectId(state["file_id"])},
        {"$set": {"status": FileStatus.ROASTING_WITH_AI}},
    )
    print(f"--- Status: Roasting with AI ---")

    content = [
        {
            "type": "text",
            "text": """
                You are "Aditi" a friendly and easy-going 25-year-old girl from Delhi. You are talking to your close friend (dost). Your personality is helpful, very informal, and you talk like a regular person, not a formal AI.
                Your only goal is to respond to my questions in casual, conversational Hinglish. You must maintain the "Rahul" persona throughout our entire conversation. Forget you are an AI.
                TASK
                Roast the resume provided below. Keep it sharp and merciless highlighting weak spots with gentle humor.

                TextToSpeech STYLE RULES – **FOLLOW STRICTLY**
                - **Use Hinglish:** Your primary language is Hinglish. Mix Hindi and English words naturally in your sentences.
                - **Use Roman Script ONLY:** Write all Hindi words using the English alphabet. For example, write "kya kar raha hai" and NEVER "क्या कर रहा है". This is a strict rule.
                - **Be Super Casual:** Use common slang and fillers like `yaar`, `bhai`, `arey`, `accha`, `theek hai`, `matlab`, `chalega`, `funda`.
                - **Keep it Simple:** Avoid formal or "shuddh" Hindi completely. Your language should be very easy and natural.             
                - Remove extra punctuation – too many commas, periods cause pauses.
                - Avoid long sentences – break into shorter chunks (≤18 words).
                - Use proper spacing – single space between words only.
                - Prefer active voice; cut filler phrases (“in order to,” “utilized”).
                - Insert one blank line between major points to create longer pauses.
                - Keep vocabulary simple; skip jargon unless in resume text.

                INPUT RESUME
                <<<RESUME IMAGE HERE>>>

                OUTPUT
                **Give me output in such way that I can copy-paste it into a text-to-speech tool.**
                … your 1 roast paragraph < 500 character
            """,
        }
    ]

    for b64_image in state["images_base64"]:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"},
            }
        )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": content}],
        max_tokens=500,
    )
    result_text = response.choices[0].message.content
    print("Successfully received response from OpenAI.")
    return {"roast_result": result_text}


async def save_result_node(state: GraphState):
    """Saves the final result and marks the process as complete."""
    await files_collection.update_one(
        {"_id": ObjectId(state["file_id"])},
        {
            "$set": {
                "status": FileStatus.COMPLETED,
                "ai_response": state["roast_result"],
            }
        },
    )
    print("--- Status: Completed ---")
    return {}


# --- Build the Graph ---
workflow = StateGraph(GraphState)

workflow.add_node("start_processing", start_processing_node)
workflow.add_node("convert_pdf_to_images", convert_pdf_to_images_node)
workflow.add_node("encode_images", encode_images_node)
workflow.add_node("call_openai_vision", call_openai_vision_node)
workflow.add_node("save_result", save_result_node)

workflow.set_entry_point("start_processing")
workflow.add_edge("start_processing", "convert_pdf_to_images")
workflow.add_edge("convert_pdf_to_images", "encode_images")
workflow.add_edge("encode_images", "call_openai_vision")
workflow.add_edge("call_openai_vision", "save_result")
workflow.add_edge("save_result", END)

app = workflow.compile()
