from concurrent.futures import process
import multiprocessing
from web_search import google_results

import psutil

import concurrent.futures

search_these = [
    "Parsing made easy",
    "Create paper planes",
    "New searching methods"
]

processes = []
if __name__ == '__main__':
    for i in search_these:
        print(multiprocessing.current_process.getName())
        p = multiprocessing.Process(name = "google_results",target=google_results,args=(i,))
        p.start()
        processes.append(p)
        

# with concurrent.futures.ThreadPoolExecutor() as executor:
# processes = []
# # pids = []
# for i in search_these:
#     # while(True):
#     #     print("inside?")
#     #     if(len(pids) > 1):
#     #         # pids[0].terminate
#     #         killme=pids[0].terminate()
#     #         killme.terminate()
#     #     else:
#     #         break
#     p = multiprocessing.Process(target=google_results,args=(i,))
#     p.start()
#     # pids.append(p.pid)
#     processes.append(p)

