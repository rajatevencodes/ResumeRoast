import { initializeViewport } from "./viewport.js";
import { initializeFileUpload } from "./fileUpload.js";
import { initializeMainFeatures } from "./eventHandlers.js";

export function initializeApp() {
  initializeViewport();
  initializeFileUpload(initializeMainFeatures);
}
