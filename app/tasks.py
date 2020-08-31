import time
from rq import get_current_job
from swagger.swaggerJob import SwaggerJob


def example(seconds):
    job = get_current_job()
    print("Starting task")
    for i in range(seconds):
        job.meta["progress"] = 100.0 * i / seconds
        job.save_meta()
        print(i)
        time.sleep(1)
    job.meta["progress"] = 100
    job.save_meta()
    print("Task completed")


def swagger():
    job = get_current_job
    print("+++ Starting Swagger Job +++")
    SwaggerJob.run_job()
    # run_job()
    print("=== Swagger Job Completed ===")


def nexus():
    job = get_current_job()
    print("Starting NexusIQ task...")


def leaks():
    job = get_current_job()
    print("+++ Starting Secret/Leaks scanning... +++")
    print(" xxx - NOT YET IMPLEMENTED - xxx")
    print("=== Scanning completed ===")
