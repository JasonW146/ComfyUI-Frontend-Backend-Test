// Frontend/Client

// Imports the "api" object from the ComfyUI api.js module that handles backend-sent messages.
import { api } from "../../scripts/api.js"

let popup = null

// The function for creating a popup.
function showPopup(message) {

    // In case popup already existed due to a prior screw up, remove it now.
    if (popup) popup.remove()

    // Create HTML elements and design them with CSS.
    popup = document.createElement("div")
    popup.style = `
        position: fixed; top: 40%; left: 50%;
        transform: translate(-50%, -50%);
        background: white; border: 2px solid black;
        padding: 20px; z-index: 9999;
        text-align: center;
    `

    popup.innerHTML = `
        <p>${message}</p>
        <button id="continueBtn">Continue</button>
    `

    document.body.appendChild(popup)

    /* If continueBtn was clicked, send an HTTP request (client to server) that sends information to the backend (POST).
       fetch() is non-blocking, so it continues even before getting a response from the server.
       fetch() returns a Promise<Response> object while the HTTP request is sent and is being handled by the backend.
       This Promise<Response> object acts as a placeholder with which .then can not proceed yet.
       Only once an HTTP response is received, it resolves Promise<Response> into a Response object and now the code proceeds with .then(...). */
    document.getElementById("continueBtn").addEventListener("click", () => {
        fetch("/wait-node-response", { method: "POST" }).then(() => {
            popup.remove()
        })
    })
}

/* This registers a new EventListener for the event name "wait-popul". It will hold out to receive a server emitted message "wait-popup".
   Its arguments are the name of the event and its handler function. In said event occurs, the api object creates a CustomEvent object
   with the argument received from the server and dispatch it under the variable name "event". showPopup() is called and as an argument
   either gets the value under the key-name "message" that was sent from the server, if there is such a value, or it will receive "Continue?" */
   
   // "?" in this context means "If there is no value return 'undefined' instead". "||" in such a context means "Use the former value if it exists, otherwise use the latter value."
api.addEventListener("wait-popup", (event) => {
    showPopup(event.detail?.message || "Continue?")
})
