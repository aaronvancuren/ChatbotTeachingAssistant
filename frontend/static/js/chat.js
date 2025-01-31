window.addEventListener("load", () => {
    let preloads = document.querySelectorAll('article');
    for (let i = 0; i < preloads.length; i++) {
        preloads[i].innerHTML = RenderMarkdown(preloads[i].innerHTML.trim());
    }
    preloads[preloads.length-1].scrollIntoView({ behavior: "smooth", block:"end" });
});

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
            newChat.href = `/chat?chatID=${data}`;
            newChat.innerText = 'New Chat';
            for (const child of host.children) {
                child.classList.remove('active');
            }
            host.insertBefore(newChat, host.firstChild);
            while (document.getElementById('conversation').children.length > 1) {
                document.getElementById('conversation').removeChild(document.getElementById('conversation').lastChild);
            }

            let updateChat = new URLSearchParams(window.location.search);
            updateChat.set('chatID', data);
            window.history.replaceState('', '', window.location.origin + window.location.pathname + '?' + updateChat.toString());
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
            currentConversationId: new URLSearchParams(window.location.search).get('chatID').toString()
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
            document.getElementById("LOADER").display = "none";
            createChatBubble(conversation.at(-1)["content"], ["btm-left", "teaching_assistant"]);
            document.getElementById("question").value = "";
            document.getElementById("question").disabled = false;
        },
        statusCode:  {
            405: (value) => {
                alert("Error: " + JSON.parse(value.responseText).detail);
            },
            401: (value) => {
                alert("Error 401: Unauthorised");
            }
        }
    });
    createChatBubble(document.getElementById("question").value, ["btm-right", "student"]);
    document.getElementById("question").disabled = true;
    document.getElementById("LOADER").display = "block";
    try {
        document.removeChild(document.getElementById("EMPTY"));
    } catch {}
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

    displayContainer.innerHTML = RenderMarkdown(dialogue);

    container.appendChild(displayContainer);
    containerWrapper.appendChild(container);
    wrapper.appendChild(containerWrapper);
    containerWrapper.scrollIntoView({ behavior: "smooth", block:"end" });
}

function RenderMarkdown(text) {
    let markdownToHTML = new showdown.Converter();
    return markdownToHTML.makeHtml(text);
}

function updateDisclaimer(){
    let target = document.getElementById('disclaimer')
    let newVal = document.getElementById('openai_model').options[document.getElementById('openai_model').selectedIndex].text;
    target.innerText = newVal + " is an AI and will occassionally make mistakes.";
    document.getElementById('openai_model').title = document.getElementById('openai_model').options[document.getElementById('openai_model').selectedIndex].title;
}