import { addFastAnimation } from "./animations.js";
import { startSpeech } from "./speech.js";

export function initializeSpeedButton(speedButton, circle) {
  if (!speedButton) return;
  speedButton.addEventListener("click", () => {
    addFastAnimation(circle);
  });
}

export function initializePlayButton(playButton, circle) {
  if (!playButton) return;
  playButton.addEventListener("click", () => {
    startSpeech(playButton, circle);
  });
}

export function initializeMainFeatures() {
  const speedButton = document.querySelector(".speed-button");
  const circle = document.querySelector(".circle");
  const playButton = document.getElementById("play");

  initializeSpeedButton(speedButton, circle);
  initializePlayButton(playButton, circle);
}
