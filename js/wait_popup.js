import { api } from "../../scripts/api.js"

let popup = null

function showPopup(message) {
    if (popup) popup.remove()

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

    document.getElementById("continueBtn").addEventListener("click", () => {
        fetch("/wait-node-response", { method: "POST" }).then(() => {
            popup.remove()
        })
    })
}

// Listen for server-triggered messages
api.addEventListener("wait-popup", (event) => {
    showPopup(event.detail?.message || "Continue?")
})
