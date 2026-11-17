"use strict";

const button = document.querySelector(".copy");
const status = document.querySelector(".copy-status");

if (button && status) {
  button.addEventListener("click", () => {
    const command = button.getAttribute("data-copy") || "";
    if (!command) {
      return;
    }
    const done = () => { status.textContent = "Copied: " + command; };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(command).then(done, () => {
        status.textContent = "Copy unavailable. Select the command manually.";
      });
    } else {
      status.textContent = "Copy unavailable. Select the command manually.";
    }
  });
} else {
  if (status) {
    status.textContent = "";
  }
}
