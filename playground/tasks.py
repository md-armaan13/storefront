from datetime import datetime, timedelta
import time
import dramatiq


@dramatiq.actor
def print_task(seconds):
    print("Starting task")
    for num in range(seconds):
        print(num, ". Hello World!")
        time.sleep(10)
    print("Task completed")



@dramatiq.actor
def print_numbers(seconds):
    print("Starting num task")
    for num in range(seconds):
        print(num)
        time.sleep(10)
    print("Task to print_numbers completed")