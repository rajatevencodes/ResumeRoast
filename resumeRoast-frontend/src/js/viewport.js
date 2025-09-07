export function updateViewport() {
  document.documentElement.style.setProperty(
    "--dvh",
    `${window.innerHeight * 0.01}px`
  );
  document.documentElement.style.setProperty(
    "--dvw",
    `${window.innerWidth * 0.01}px`
  );
}

export function initializeViewport() {
  updateViewport();
  window.addEventListener("resize", updateViewport);
  window.addEventListener("orientationchange", () => {
    setTimeout(updateViewport, 100);
  });
}
