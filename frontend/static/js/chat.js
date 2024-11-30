function addChat() {
    $.ajax({
        type: "GET",
        url: "/addChat",    
        headers: {
            "X-victor-uid": "DEMO-1234", //Replace with UUID Cookie
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "frame-ancestors 'none'",
            "X-Frame-Options": "DENY",
        },
        success: function(data) {
            host = document.getElementById('convos');
            newChat = document.createElement('a');
            newChat.classList.add('active');
            newChat.classList.add('temporary');
            newChat.href = `/chat?chatID=${data.id}`;
            newChat.innerText = 'New Chat';
            for (const child of host.children) {
                child.classList.remove('active');
            }
            host.insertBefore(newChat, host.firstChild);
            while (document.getElementById('conversation').children.length > 1) {
                document.getElementById('conversation').removeChild(document.getElementById('conversation').lastChild);
            }
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

function AskQuestion() {
    $.ajax({
        type: "POST",
        url: "/ask",
        data: JSON.stringify({
            user_content: document.getElementById("question").value,
            openai_model: document.getElementById('openai_model').value,
            context: document.getElementById('context').value,
            currentConversation: new URLSearchParams(window.location.search).get('chatID')
        }),        
        headers: {
            "X-victor-uid": "DEMO-1234", //Replace with UUID Cookie
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "frame-ancestors 'none'",
            "X-Frame-Options": "DENY",
            "Content-Type": "application/json"
        },
        success: function(data) {
            conversation = JSON.parse(data);
            createChatBubble(document.getElementById("question").value, ["btm-right", "student"]);
            createChatBubble(conversation.at(-1)["content"], ["btm-left", "teaching_assistant"]);
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
    
    if (classes.includes('teaching_assistant')) {
        chatWrapper.innerText = `${document.getElementById('openai_model').options[document.getElementById('openai_model').selectedIndex].text} says...`;
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
    let newVal = document.getElementById('teaching_assistant').options[document.getElementById('teaching_assistant').selectedIndex].text;
    target.innerText = target.innerText.replace(/[^\s]*/, newVal);
    document.getElementById('teaching_assistant').title = document.getElementById('TAs').options[document.getElementById('teaching_assistant').selectedIndex].title;
}