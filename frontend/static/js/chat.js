function AskQuestion() {
    console.log(document.getElementById("question").value)
    $.ajax({
        type: "POST",
        url: "/ask",
        data: document.getElementById("question").value,
        headers: {
            "X-victor-uid": "DEMO-1234", //Replace with UUID Cookie
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "frame-ancestors 'none'",
            "X-Frame-Options": "DENY",
        },
        success: function(data) {
            GenerateElement(document.getElementById("question").value, "DEMO-1234");
            GenerateElement(data.chat);
            document.getElementById("question").value = "";
        },
        error: function(error) {
            console.log("Error!", error);
            switch (code) {
                case 400:
                    alert(error);
                    break;
                case 500:
                    alert(error);
                    break;
            }
        }
    })


}

function GenerateElement(dialogue, SPEAKER = "Victor"){
    console.log(SPEAKER, " said ", dialogue);
    wrapper = document.getElementById("conversation");
    
    container = document.createElement("div");
    if (SPEAKER === "Victor") {
        container.classList.add("talk-bubble", "tri-right", "btm-left", "victor");
    } else {
        container.classList.add("talk-bubble", "tri-right", "btm-right", "user");
    }

    displayContainer = document.createElement("div");
    displayContainer.classList.add("talktext");

    dialogueContainer = document.createElement("p");
    dialogueContainer.innerText = dialogue;
    
    displayContainer.appendChild(dialogueContainer);
    container.appendChild(displayContainer);
    wrapper.appendChild(container);

}