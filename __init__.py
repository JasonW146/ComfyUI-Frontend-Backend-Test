from .wait_node import WaitNode

NODE_CLASS_MAPPINGS = {"WaitNode": WaitNode}

# Registering the JS files for the browser to be aware of.
WEB_DIRECTORY = "./js"

__all__ = ['NODE_CLASS_MAPPINGS', 'WEB_DIRECTORY']

