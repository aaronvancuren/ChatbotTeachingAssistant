function callChat(){
    $.ajax({
        url: process.env.HOST + "/"+ process.env.PORT + "/chat",
        success: (data) => {
            result.innerHTML = "Chatbot response: " + data
        },
        statusCode: {
            400: (data) => {
                console.log(data)
            },
            500: (data) => {
                console.log(data)
            }
        }
    })
}
