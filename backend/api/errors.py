from fastapi import HTTPException

ERRORMESSAGES = {
    400: "It looks like your request skipped class.",
    401: "You need a valid student ID to enter this party… I mean, page.",
    403: "Sorry, professor’s office hours are closed. No sneaking in!",
    404: "Page not found? It’s probably taking a break. Try again later!",
    405: "That’s not how we do things here. Read the syllabus!",
    406: "Just like that essay without citations—your request doesn’t meet the required format.",
    407: "You need permission from the TA before you can access this!",
    408: "The server waited as long as possible, but your request missed the deadline!",
    422: "It’s like trying to process a math equation without numbers. Nope, not happening.",

    500: "This server just pulled an all-nighter and crashed. Try again later!",
    502: "Looks like the network’s having a bad day—kind of like a Wi-Fi outage during finals week.",
    503: "The server is taking a mental health day. Come back later!",
    504: "The server had to go to office hours and never came back. Please try again later.",
}

class HTTPError(HTTPException):

    message = "An error occurred"

    def __init__(self, status_code: int, detail: str):
        self.message = ERRORMESSAGES[status_code] 
        super().__init__(status_code=status_code, detail=detail)
    
    