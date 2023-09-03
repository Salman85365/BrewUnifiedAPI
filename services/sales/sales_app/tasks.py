from celery import shared_task

@shared_task
def some_long_running_task(item_id):
    # Do something time-consuming
    pass
