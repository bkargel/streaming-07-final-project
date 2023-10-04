import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Generate fake data for 35 students and 10 assignments each
class_size = 35
num_assignments = 12
percent_low_grades = 10  # Percentage of grades between 0 and 69

data = []

# Function to generate a unique 7-digit student number
def generate_student_number():
    return '003' + str(random.randint(100000, 999999))

# Generate grades for each student
for student_number in range(1, class_size + 1):
    last_name = fake.last_name()
    first_name = fake.first_name()
    student_number = generate_student_number()

    for j in range(num_assignments):
        assignment_date = fake.date_time_between(start_date='-90d', end_date='now').strftime('%Y-%m-%d')

        # Assign 15% of grades between 0 and 69, and the rest between 70 and 100
        if random.randint(1, 100) <= percent_low_grades:
            grade = random.randint(0, 69)
        else:
            grade = random.randint(70, 100)

        data.append({
            'student_number': student_number,
            'last_name': last_name,
            'first_name': first_name,
            'assignment_date': assignment_date,
            'grade': grade
        })

# Print the generated data
for i, entry in enumerate(data, start=1):
    print(f'Student {entry["student_number"]}: {entry["first_name"]} {entry["last_name"]}, '
          f'Assignment Date: {entry["assignment_date"]}, Grade: {entry["grade"]}%')
