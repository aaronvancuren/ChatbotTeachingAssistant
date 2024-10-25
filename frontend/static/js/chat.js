var chatbot = [];

function AskQuestion() {
    $.ajax({
        type: "POST",
        url: "/ask",
        data: JSON.stringify({
            chatbot: chatbot,
            user_content: document.getElementById("question").value
        }),        
        headers: {
            "X-victor-uid": "DEMO-1234", //Replace with UUID Cookie
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "frame-ancestors 'none'",
            "X-Frame-Options": "DENY",
            "Content-Type": "application/json"
        },
        success: function(data) {
            chatbot = JSON.parse(data);
            createChatBubble(document.getElementById("question").value, ["btm-right", "user"]);
            createChatBubble(chatbot[chatbot.length - 1][1], ["btm-left", "victor"]);
            document.getElementById("question").value = "";
        },
        statusCode:  {
            405: (value) => {
                alert("Error: " + JSON.parse(value.responseText).detail);
            },
            401: (value) => {
                alert("Error 401: Unauthorised");
            }
        }
    })
}

function createChatBubble(dialogue, classes){
    wrapper = document.getElementById("conversation");
    
    container = document.createElement("div");
    container.classList.add("talk-bubble", "tri-right", ...classes);
        
    displayContainer = document.createElement("div");
    displayContainer.classList.add("talktext");

    dialogueContainer = document.createElement("p");
    dialogueContainer.innerText = dialogue;
    
    displayContainer.appendChild(dialogueContainer);
    container.appendChild(displayContainer);
    wrapper.appendChild(container);
}