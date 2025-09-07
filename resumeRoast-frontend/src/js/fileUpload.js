import { startSpeech } from "./speech.js";

export function validateFile(file) {
  if (file.size > 5 * 1024 * 1024) {
    alert("File size must be less than 5MB");
    return false;
  }
  return true;
}

// step 1: Helper to show/hide sections
function showSection(sectionId) {
  document.getElementById("upload-section").classList.add("hidden");
  document.getElementById("progress-section").classList.add("hidden");
  document.getElementById("main-content").classList.add("hidden");
  document.getElementById(sectionId).classList.remove("hidden");
}

// step 2: Helper to update progress message
function setProgressMessage(msg) {
  document.getElementById("progress-message").textContent = msg;
}

// step 3: Store roast text globally
let roastText = "";
export function getRoastText() {
  return roastText;
}

// step 4: Main upload handler
export async function handleFileUpload(event, onComplete) {
  const file = event.target.files[0];
  if (!file || !validateFile(file)) return;

  // Show progress section
  showSection("progress-section");
  setProgressMessage("Processing...");

  // Upload file to /upload and get file_id
  let file_id = null;
  const formData = new FormData();
  formData.append("file", file);
  try {
    const res = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    file_id = data.file_id;
    if (!file_id) {
      setProgressMessage("Error: Backend did not return a file_id.");
      return;
    }
  } catch (e) {
    setProgressMessage("Error: Could not connect to backend.");
    return;
  }

  // Poll /{file_id} for ai_response and show backend status
  let aiResponse = null;
  try {
    let status = null;
    for (let i = 0; i < 10; i++) {
      const res = await fetch(`http://localhost:8000/${file_id}`);
      const data = await res.json();
      status = data.status;
      if (data.ai_response) {
        aiResponse = data.ai_response;
        break;
      }
      setProgressMessage(status || "Processing...");
      await new Promise((r) => setTimeout(r, 1500));
    }
    if (!aiResponse) {
      setProgressMessage("Error: AI response not ready.");
      return;
    }
    roastText = aiResponse;
  } catch (e) {
    setProgressMessage("Error: Could not get AI response.");
    return;
  }

  // Show main content
  showSection("main-content");
  // Start speech automatically
  const circle = document.querySelector(".circle");
  startSpeech(null, circle);
  onComplete();
}

export function initializeFileUpload(onComplete) {
  const fileInput = document.getElementById("resume-upload");
  fileInput.addEventListener("change", (event) =>
    handleFileUpload(event, onComplete)
  );
}
