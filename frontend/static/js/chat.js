var chatbot = [];

function AskQuestion() {
    $.ajax({
        type: "POST",
        url: "/ask",
        data: JSON.stringify({
            chatbot: chatbot,
            user_content: document.getElementById("question").value,
            ta: document.getElementById('TAs').value
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
            createChatBubble(document.getElementById("question").value, ["btm-right", "student"]);
            createChatBubble(chatbot[chatbot.length - 1][1], ["btm-left", "ta"]);
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
    
    containerWrapper = document.createElement("div");
    containerWrapper.classList.add('talk-bubble');
    chatWrapper = document.createElement("p");
    
    if (classes.includes('ta')) {
        chatWrapper.innerText = `${document.getElementById('TAs').options[document.getElementById('TAs').selectedIndex].text} says...`;
        containerWrapper.classList.add('left');
        chatWrapper.classList.add('left')
    } else {
        chatWrapper.innerText = 'You asked...';
        containerWrapper.classList.add('right');
        chatWrapper.classList.add('right')
    }

    chatWrapper.classList.add('text-from')
    containerWrapper.appendChild(chatWrapper);

    container = document.createElement("div");
    container.classList.add("tri-right", ...classes);
        
    displayContainer = document.createElement("div");
    displayContainer.classList.add("talktext");

    dialogueContainer = document.createElement("p");
    dialogueContainer.innerText = dialogue;
    
    displayContainer.appendChild(dialogueContainer);
    container.appendChild(displayContainer);
    containerWrapper.appendChild(container);
    wrapper.appendChild(containerWrapper);
}

function updateDisclaimer(){
    let target = document.getElementById('Disclaimer')
    let newVal = document.getElementById('TAs').options[document.getElementById('TAs').selectedIndex].text;
    target.innerText = target.innerText.replace(/[^\s]*/, newVal);
}