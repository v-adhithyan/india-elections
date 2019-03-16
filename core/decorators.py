import functools
import time


def profile_endpoint(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        return_value = func(*args, **kwargs)
        end = time.time()

        if isinstance(return_value, dict):
            total_time = end - start
            return_value.update({'time_taken_in_seconds': round(total_time, 2)})

        return return_value

    return wrapper
