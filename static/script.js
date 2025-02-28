async function sendMessage() {
  let inputField = document.getElementById("message-input");
  let chatMessages = document.getElementById("chat-messages");
  let loader = document.getElementById("loader");

  let userMessage = inputField.value;
  chatMessages.innerHTML += `<p><strong>You:</strong>${userMessage}</p>`;
  inputField.value = "";

  // Show the loader
  loader.style.display = "block";

  let response = await fetch(
    `/chat?prompt=${encodeURIComponent(userMessage)}`,
    {
      method: "POST",
    }
  );

  // Hide the loader
  loader.style.display = "none";

  if (!response.ok) {
    chatMessages.innerHTML += `<p id="error"><strong id="AI">Mistral:</strong>Error Failed to fetch response</p>`;
    return;
  }

  let data = await response.json();
  chatMessages.innerHTML += `<p id="response"><strong id="AI">Mistral:</strong>${data.response}</p>`;
  chatMessages.scrollTop = chatMessages.scrollHeight;
}
