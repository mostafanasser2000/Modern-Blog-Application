const messages = document.getElementById("messages");
const close = document.getElementById("close");

if (messages) {
  close.addEventListener("click", function () {
    messages.style.display = "none";
  });
}
