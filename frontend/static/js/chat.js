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
            newChat.classList.add('btn', 'btn-secondary', 'active', 'temporary');
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
            currentConversationId: new URLSearchParams(window.location.search).get('chatID').toString()
        }),        
        headers: {
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "frame-ancestors 'none'",
            "X-Frame-Options": "DENY",
            "Content-Type": "application/json"
        },
        success: function(data) {
            conversation = JSON.parse(data);
            document.getElementById("LOADING").classList.add("hidden");
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
            },
            429: (value) => {
                document.getElementById("LOADING").classList.add("hidden");
                createChatBubble("I'm really glad you reached out to discuss this, but unfortunately, I have to wrap up now. If you'd like to continue, you can reach out to the professor or the other TA.", ["btm-left", "teaching_assistant"]);
                document.getElementById("question").value = "";
            },
            500: (value) => {
                document.getElementById("LOADING").classList.add("hidden");
                createChatBubble("Unfortunately, I can't answer that question right now. Please try again later.", ["btm-left", "teaching_assistant"]);
                document.getElementById("question").value = "";
            }
        }
    });
    createChatBubble(document.getElementById("question").value, ["btm-right", "student"]);
    document.getElementById("question").disabled = true;
    document.getElementById("LOADING").classList.remove("hidden");
    try {
        document.getElementById("EMPTY").remove();
    } catch {}
}

function createChatBubble(dialogue, classes){
    wrapper = document.getElementById("conversation");
    
    containerWrapper = document.createElement("div");
    containerWrapper.classList.add('talk-bubble');
    chatWrapper = document.createElement("p");
    
    if (classes.includes('teaching_assistant')) {
        chatWrapper.innerText = `John says...`;
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
    if (classes.includes('teaching_assistant')) {

        feedbackWrapper = document.createElement("div");
        feedbackWrapper.classList.add("feedback");

        speak = document.createElement("a");
        speak.classList.add("bi", "bi-volume-up");

        good = document.createElement("a");
        good.classList.add("bi", "bi-hand-thumbs-up");

        bad = document.createElement("a");
        bad.classList.add("bi", "bi-hand-thumbs-down");

        feedbackWrapper.appendChild(speak);
        feedbackWrapper.appendChild(bad);
        feedbackWrapper.appendChild(good);
        wrapper.appendChild(feedbackWrapper);
    }
    containerWrapper.scrollIntoView({ behavior: "smooth", block:"end" });
}

function RenderMarkdown(text) {
    let markdownToHTML = new showdown.Converter();
    UpdateChatNum();
    return markdownToHTML.makeHtml(text);
}

function UpdateChatNum() {
    try {
        let log = JSON.parse(atob(document.cookie.split('=')[1].slice(2).split("").reverse().join("").slice(1)))
        document.getElementById("counter").innerHTML = 'Daily Questions Left: ' + (log.max - log.count) + '/' + log.max;
    } catch {}
}