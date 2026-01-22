function sendMessage() {
    const input = document.getElementById("userInput");
    const chatBox = document.getElementById("chatBox");
    const message = input.value.trim();

    if (message === "") return;

    chatBox.innerHTML += `<p class="user">You: ${message}</p>`;
    input.value = "";

    fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        chatBox.innerHTML += `<p class="bot">Bot: ${data.answer}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(() => {
        chatBox.innerHTML += `<p class="bot">Bot: Server error</p>`;
    });
}