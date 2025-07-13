# Backend/Server

''' server is a ComfyUI module that handles the ComfyUI built-in HTTP server and the messaging between backend and frontend.
    PromptServer is a singleton class that provides access to routes and sync_send.'''
from server import PromptServer
''' aiohttp is an asynchronous HTTP server and client library.
    web is a web server module comparable to Flask but async native.'''
from aiohttp import web
import time
from threading import Event

wait_event = Event()

# Non-blocking function that establishes a route to handle this kind of HTTP request by the frontend.
@PromptServer.instance.routes.post("/wait-node-response")
async def wait_node_response(request):
    print("Received continue from frontend")
    # Sets internal flag to True and in this case terminates the timer.
    wait_event.set()

    ''' Creates a Response object and attaches the dict as the HTTP body. The status value 200 is a default argument.
        Afterwards it sends the HTTP response (server to client).'''
    return web.json_response({"status": "ok"})

def wait_for_continue(timeout=600):
    # Internal flag is set to false.
    wait_event.clear()
    # Give the current time in seconds and add the timeout value.
    end = time.monotonic() + timeout
    # Hold off the code from proceeding while the flag of wait_event is not set or the timer hasn't ran out yet.
    while not wait_event.is_set() and time.monotonic() < end:
        time.sleep(0.2)

# ComfyUI node.
class WaitNode:
    RETURN_TYPES = ("STRING",)
    FUNCTION = "wait"
    CATEGORY = "example"

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    def wait(self):
        ''' Synchronous function that signals to the JS event handler. It acts as a bridge between ComfyUI's frontend and backend.
            "wait-popup" is the event to be triggered here. The dictionary is a payload that is included for further information used as an argument later.'''
        PromptServer.instance.send_sync("wait-popup", {"message": "Please continue..."})
        # A timer to act as a fail-safe.
        wait_for_continue()
        return ("User continued",)
    