// Assuming your backend endpoint is '/getChatGPTResponse'
const API_URL = '/getResponse';

document.addEventListener("DOMContentLoaded", () => {
  const inputField = document.getElementById("input");
  inputField.addEventListener("keydown", function (e) {
    if (e.code === "Enter") {
      let input = inputField.value.trim();
      if (input) {
        output(input);
        inputField.value = "";
      }
    }
  });
});

function output(input) {
  addChat(input, "Cevap bekleniyor..."); // To provide some feedback while waiting for the response
  
  // Fetch response from backend which in turn communicates with ChatGPT
  fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({message: input})
  })
  .then(response => response.json())
  .then(data => {
    // Update the message with the actual response
    const botMessages = document.querySelectorAll("#bot-response");
    const lastBotMessage = botMessages[botMessages.length - 1];
    lastBotMessage.textContent = data.reply;
    voiceControl(data.reply);
  })
  .catch(error => {
    console.error("Error:", error);
  });
}

function addChat(input, product) {
  const mainDiv = document.getElementById("message-section");
  
  let userDiv = document.createElement("div");
  userDiv.id = "user";
  userDiv.classList.add("message");
  userDiv.innerHTML = `<span id="user-response">${input}</span>`;
  mainDiv.appendChild(userDiv);

  let botDiv = document.createElement("div");
  botDiv.id = "bot";
  botDiv.classList.add("message");
  botDiv.innerHTML = `<span id="bot-response">${product}</span>`;
  mainDiv.appendChild(botDiv);

  var scroll = document.getElementById("message-section");
  scroll.scrollTop = scroll.scrollHeight;
}
