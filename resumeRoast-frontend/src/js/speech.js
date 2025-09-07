import { getRoastText } from "./fileUpload.js";

export function resetButtonState(button) {
  if (!button) return;
  button.disabled = false;
  button.textContent = "Speak with options!";
}

export function handleSpeechSuccess(audio, playButton, circle) {
  audio.volume = 1;
  audio.play();

  audio.addEventListener("ended", function () {
    setTimeout(() => {
      resetButtonState(playButton);
      circle.classList.remove("speaking");
    }, 500);
  });

  audio.addEventListener("error", function () {
    resetButtonState(playButton);
    circle.classList.remove("speaking");
  });
}

export function setTitleText(text, isError = false) {
  const titleEl = document.querySelector(".title");
  if (titleEl) {
    titleEl.textContent = text;
    if (isError) {
      titleEl.style.color = "#ff3333";
      titleEl.style.background = "rgba(255,0,0,0.07)";
      titleEl.style.borderRadius = "12px";
      titleEl.style.padding = "clamp(10px, 4vw, 18px) clamp(12px, 6vw, 24px)";
      titleEl.style.fontWeight = "bold";
      titleEl.style.boxShadow = "0 2px 16px rgba(255,0,0,0.08)";
      titleEl.style.marginTop = "clamp(16px, 6vw, 32px)";
      titleEl.style.fontFamily =
        'Gilroy, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif';
      titleEl.style.fontSize = "clamp(0.8rem, 3vw, 1.3rem)";
      titleEl.style.lineHeight = "1.4";
      titleEl.style.wordBreak = "break-word";
    } else {
      titleEl.removeAttribute("style");
    }
  }
}

export function handleSpeechError(error, playButton, circle) {
  console.error("Speech error:", error, JSON.stringify(error));
  resetButtonState(playButton);
  circle.classList.remove("speaking");
  // Show the AI response (roast text) in a neat way
  const roastText = getRoastText();
  setTitleText(roastText || "Sorry, something went wrong with speech.", true);
  // Hide the circle if speech fails
  if (circle) {
    circle.style.display = "none";
  }
}

export async function startSpeech(playButton, circle) {
  if (playButton) {
    playButton.disabled = true;
    playButton.textContent = "Speaking...";
  }
  circle.classList.add("speaking");

  try {
    const text = getRoastText();
    if (!text || text.trim() === "") {
      handleSpeechError(
        { success: false, error: { message: "No text to speak" } },
        playButton,
        circle
      );
      return;
    }
    const audio = await puter.ai.txt2speech(text, {
      voice: "Aditi",
      // engine: "neural",
      language: "hi-IN",
    });

    handleSpeechSuccess(audio, playButton, circle);
  } catch (error) {
    handleSpeechError(error, playButton, circle);
  }
}
