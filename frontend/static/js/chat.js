window.addEventListener("load", () => {
    let preloads = document.querySelectorAll('article');
    for (let i = 0; i < preloads.length; i++) {
        preloads[i].innerHTML = RenderMarkdown(preloads[i].innerHTML.trim());
    }
    preloads[preloads.length-1].scrollIntoView({ behavior: "smooth", block:"end" });
});

function addChat() {
    $.ajax({
        type: "POST",
        url: "/addChat",
        data: JSON.stringify({
            model: $('input[name="ai_list"]:checked')[0].id
        }),
        headers: {
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "frame-ancestors 'none'",
            "X-Frame-Options": "DENY",
        },
        success: function(data) {
            window.location.href = data;            
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
    $('#chooseTA').modal('hide');
}

function AskQuestion() {
    $.ajax({
        type: "POST",
        url: "/ask",
        data: JSON.stringify({
            user_content: document.getElementById("question").value,
            currentConversationId: new URLSearchParams(window.location.search).get('chatID').toString(),
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
    createChatBubble(document.getElementById("question").value.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'), ["btm-right", "student"]);
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
        chatWrapper.text = `${document.getElementById("openai_model").text} says...`;
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
        let log = JSON.parse(atob(decodeURIComponent(document.cookie).split(';').find((e)=>{return e.includes("chat_usage")}).trim().substring(14).split("").reverse().join("").substring(2)));
        document.getElementById("counter").innerHTML = 'Daily Questions Left: ' + (log.max - log.count) + '/' + log.max;
        if (log.max - log.count === 0)
            document.getElementById("question").disabled = true;
    } catch{}
}