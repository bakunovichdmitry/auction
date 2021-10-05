from celery import shared_task


@shared_task
def update_price(frequency, step): # naming???
    print('Hello')
