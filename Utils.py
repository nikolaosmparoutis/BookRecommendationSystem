
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

#other way
def remove_bad_char(self, col_to_remove_char, char_to_rm):
    for counter in range(0, len(self.df[col_to_remove_char])):
        self.df.loc[counter, col_to_remove_char] = self.df.loc[counter, col_to_remove_char].replace(char_to_rm,"")
