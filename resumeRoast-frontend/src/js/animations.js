export function addFastAnimation(circle) {
  circle.classList.add("fast");
  setTimeout(() => {
    circle.classList.remove("fast");
  }, 3000);
}

export function addSpeakingAnimation(circle) {
  circle.classList.add("speaking");
}

export function removeSpeakingAnimation(circle) {
  circle.classList.remove("speaking");
}
