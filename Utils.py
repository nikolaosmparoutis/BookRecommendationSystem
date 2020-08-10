
def calculate_execution_time():
    import time
    start_time = time.time()
    # Code here
    print("--- %s seconds ---", time.time() - start_time)


def calculate_memory_until_here():
    import os
    import psutil
    process = psutil.Process(os.getpid())
    print("Memory in KB" , process.memory_info().rss/1024)  # in Kilobyte
