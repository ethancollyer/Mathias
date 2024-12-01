import multiprocessing


def get_tools():
    tools = [{
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "takes an equation string as an input, parses the equation string into sympy expressions, then returns the computed solution.",
            "parameters": {
                "type": "object",
                "properties": {
                    "equation": {
                        "type": "string",
                        "description": "the mathmatical expression that needs to be computed. e.g. 3*x**2 = asin(16) / 4",
                    },
                },
                "required": ["equation"],
            },
        },
    }]

    return tools

def worker(func, result_queue, *args):
    """Worker function to run the task in the timeout function."""
    try:
        result = func(*args)
        result_queue.put(result)  # Put result into queue
    except Exception as e:
        result_queue.put(e)  # If an exception occurs, put it into the queue

def with_timeout(timeout_seconds, func, *args):
    """Run the function with a timeout."""
    # Create a Queue for communication between processes
    result_queue = multiprocessing.Queue()
    
    # Create a separate process to run the function
    process = multiprocessing.Process(target=worker, args=(func, result_queue, *args))
    process.start()

    # Wait for the result with a timeout
    process.join(timeout=timeout_seconds)
    
    # If process is still alive after the timeout, terminate it
    if process.is_alive():
        process.terminate()
        process.join()
        raise TimeoutError(f"Function execution exceeded {timeout_seconds} seconds.")
    
    # Get result from the queue (this is where the result is passed back)
    result = result_queue.get_nowait() if not result_queue.empty() else None
    
    if isinstance(result, Exception):
        raise result  # Reraise the exception from the worker if it occurred

    return result

