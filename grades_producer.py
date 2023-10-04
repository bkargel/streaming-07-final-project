"""
    This program generates fake student data with the student number, student last name, student first name,
    the date the assignment was submitted, and the grade as a percentage. Then, each line of data is sent to
    the queue "student_grades" for consumption, with one line sent every 5 seconds. 
    
    Author: Brendi Kargel
    Date: October 3, 2023

"""
import random
from faker import Faker
from datetime import datetime, timedelta
from operator import itemgetter
import pika
import sys
import webbrowser
import time

fake = Faker()

# Declare program constants (typically constants are named with ALL_CAPS)

HOST = "localhost"
PORT = 9999
ADDRESS_TUPLE = (HOST, PORT)

# Generate fake data for 50 students and 15 assignments each
class_size = 50
num_assignments = 15

percent_low_grades = 5  # Percentage of grades between 1 and 59
percent_zeros = 2 # Percentage of grades that are zeros

start_date = datetime(2023, 8, 14)
end_date = datetime.now()

data = []

# Function to generate a unique 7-digit student number
def generate_student_number():
    return '003' + str(random.randint(100000, 999999))

# Generate grades for each student
def generate_data():
    for student_number in range(1, class_size + 1):
        last_name = fake.last_name()
        first_name = fake.first_name()
        student_number = generate_student_number()

        for j in range(num_assignments):
            assignment_date = fake.date_time_between(start_date + timedelta(days=random.randint(0, (end_date - start_date).days))).strftime('%Y-%m-%d')

            # Assign 2% of grades as zero, 5% between 1 and 59, and the rest between 60 and 100
            if random.randint(1, 100) <= percent_zeros:
                grade = 0
            elif random.randint(1, 100) <= percent_low_grades:
                grade = random.randint(1, 59)
            else:
                grade = random.randint(60, 100)

            data.append({
                'student_number': student_number,
                'last_name': last_name,
                'first_name': first_name,
                'assignment_date': assignment_date,
                'grade': grade
            })


# Delare variable for queue
queue = "student_grades"

# Only opens the Admin website if show_offer = True
show_offer = False

def offer_rabbitmq_admin_site():
    """Offer to open the RabbitMQ Admin website"""
    global show_offer
    if show_offer:
        webbrowser.open_new("http://localhost:15672/#/queues")

# Function to send the messages to the queue       
def send_message():
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue (str): name of the queue
        message (str): the message to be sent to the queue
    """

    try:
        # Shuffle the data to randomize the order
        random.shuffle(data)
        # Sort the data by assignment date in chronological order
        data.sort(key=itemgetter('assignment_date'))
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(HOST))
        # use the connection to create a communication channel
        ch = conn.channel()
        # use the channel to declare a durable queue
        ch.queue_declare(queue, durable=True)

        # create messages to send to the queues
        # convert data to a structured string format
        def format_data(entry):
            return f"{entry['student_number']},{entry['last_name']},{entry['first_name']},{entry['assignment_date']},{entry['grade']}"
        
        for entry in data:
            message = format_data(entry)

            # encode the messages
            message_encode = "," .join(message).encode()              
                
            # use the channel to publish message to the queue
            # every message passes through an exchange
            ch.basic_publish(exchange="", routing_key=queue, body=message)  

            # print message to the console for the user
            print(f" [x] Sent: {message} to {queue}")

            # Wait 5 seconds between each message
            time.sleep(5)

    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # close the connection to the server
        conn.close()

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":  
    # ask the user if they'd like to open the RabbitMQ Admin site
    offer_rabbitmq_admin_site()

    # generate the fake data
    generate_data()
    
    # Send messages to the queues
    send_message() 