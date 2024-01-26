import time
import multiprocessing as mp
import concurrent.futures as cf

from settings import cfg
from multiprocessing import Lock


lock = Lock()


def job(task, output):
    """
    return [[link_id, link, contents]]
    """
    url_id, url = task
    outer_html, check, height = check_ng_v2(url)
    with lock:
        output.append([url_id, url, outer_html, check, height])
    return output


def worker(q, output, fn=job):
    while True:
        task = q.get()
        time.sleep(0.5)
        if task is None:
            break
        # do your work here with task
        if fn:
            output = fn(task, output)

    return output


def process_pool_task(tasks, num_workers=4, max_thread_pool=4, output=None, fn=job):
    # create a process pool
    if output is None:
        output = []

    with mp.Pool(num_workers):
        # create a shared queue
        q = mp.Manager().Queue()
        # start worker threads
        with cf.ThreadPoolExecutor(max_thread_pool) as executor:
            futures = [executor.submit(worker, q, output, fn) for _ in range(max_thread_pool)]
            # add tasks to queue
            for task in tasks:
                q.put(task)
            # add sentinel values to queue to signal worker threads to terminate
            for _ in range(max_thread_pool):
                q.put(None)
            # wait for worker threads to finish
            cf.wait(futures)
    return output


def parallel_fn_v2(urls, files, n, folder_urls):
    tasks = list(zip(urls, files, n, folder_urls))
    return process_pool_task(tasks, num_workers=cfg.MAX_WORKERS, max_thread_pool=cfg.MAX_THREAD_POOL, output=[])
