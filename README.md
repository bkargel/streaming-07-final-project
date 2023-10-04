# streaming-07-final-project

This project streams faked student data to a queue every 5 seconds. The message is then picked up by the consumer and an alert is sent if the assignment grade is less than a specified threshold. For this project, that grade is below 60%.

## Prerequisites
1. Git
1. Python 3.7+ (3.11+ preferred)
1. VS Code Editor
1. VS Code Extension: Python
1. RabbitMQ installed and running locally

## Description - Producer
The grades_producer.py file contains code which fakes data for 50 students, with 15 assignments each. The following fields are generated with fake data: student_number, last_name, first_name, assignment_date, and grade. The student number is generated to always begins with "003" and is seven digits long using this code:

def generate_student_number():
    return '003' + str(random.randint(100000, 999999))
    
The grades are generated randomly within parameters:

2% of grades are zeros
5% of grades are between 1% and 59%
The remaining grades are above 60%

    if random.randint(1, 100) <= percent_zeros:
        grade = 0
    elif random.randint(1, 100) <= percent_low_grades:
        grade = random.randint(1, 59)
    else:
        grade = random.randint(60, 100)

The start and end date for generation of the assignment_date is set to the beginning of the school year and now, respectively. These variables can be changed to reflect any period of time.

start_date = datetime(2023, 8, 14)
end_date = datetime.now()
for j in range(num_assignments):
            assignment_date = fake.date_time_between(start_date + timedelta(days=random.randint(0, (end_date - start_date).days))).strftime('%Y-%m-%d')

The data is shuffled to prevent listing all 15 assignments for each student together and then streamed in chronological order by submission date:

random.shuffle(data)
data.sort(key=itemgetter('assignment_date'))

Each record is then sent to the student_grades queue, where it will wait to be received by the consumer.

Variables are utilized for the parameters in this scipt so that they can be easily changed for individualized use.

## Description - Consumer
The grades_consumer.py file contains code that reads each of the messages from the "student_grades" queue and prints an alert if the grade is below a 60%:

alert = "Alert!! Student has received a failing grade and may want to redo the assignment."

Again, variables are utilized to make changing of any of these parameters easier.

## Screenshot of concurrent processes
![Alt text](https://github.com/bkargel/streaming-07-final-project/blob/main/concurrent_processes.png?raw=true)

## Screenshot of producer sending messages

![Alt text](https://github.com/bkargel/streaming-07-final-project/blob/main/grades_producer.png?raw=true)

## Screenshots of consumer receiving messages and printing alerts

![Alt text](https://github.com/bkargel/streaming-07-final-project/blob/main/grades_consumer.png?raw=true)

## Screenshot of queue admin

![Alt text](https://github.com/bkargel/streaming-07-final-project/blob/main/queue_admin.png?raw=true)