from server import PromptServer
from aiohttp import web
import time
from threading import Event

# Global wait event (reset per invocation)
wait_event = Event()

@PromptServer.instance.routes.post("/wait-node-response")
async def wait_node_response(request):
    print("Received continue from frontend")
    wait_event.set()
    return web.json_response({"status": "ok"})

def wait_for_continue(timeout=600):
    wait_event.clear()
    end = time.monotonic() + timeout
    while not wait_event.is_set() and time.monotonic() < end:
        time.sleep(0.2)

class WaitNode:
    RETURN_TYPES = ("STRING",)
    FUNCTION = "wait"
    CATEGORY = "example"

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    def wait(self):
        # Trigger frontend popup
        PromptServer.instance.send_sync("wait-popup", {"message": "Please continue..."})
        wait_for_continue()
        return ("User continued",)
    