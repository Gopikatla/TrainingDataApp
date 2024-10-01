import json
from datetime import datetime, timedelta

# Load data from JSON file
input_file_path = r"C:\Users\sudha\OneDrive\Desktop\App\trainings (correct).txt"
output_directory = r"C:\Users\sudha\OneDrive\Desktop\App\\"

with open(input_file_path, 'r') as input_file:
    training_data = json.load(input_file)

# Task 1: Count the number of completions for each training
training_summary = {}
for trainee in training_data:
    most_recent_trainings = {}
    for record in trainee['completions']:
        training_title = record['name']
        completion_date = datetime.strptime(record['timestamp'], "%m/%d/%Y")

        # Track only the latest completion date for each training
        if training_title not in most_recent_trainings or most_recent_trainings[training_title] < completion_date:
            most_recent_trainings[training_title] = completion_date

    # Update training completion counts
    for training_title in most_recent_trainings:
        training_summary[training_title] = training_summary.get(training_title, 0) + 1

# Save output for Task 1
task_1_output_path = output_directory + "output_task_1.json"
with open(task_1_output_path, 'w') as output_file:
    json.dump(training_summary, output_file, indent=4)

# Task 2: Identify trainees who completed specific courses during a given fiscal year
target_trainings = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]
fiscal_year = 2024
fiscal_start_date = datetime(fiscal_year - 1, 7, 1)
fiscal_end_date = datetime(fiscal_year, 6, 30)

training_participants = {training: [] for training in target_trainings}
for trainee in training_data:
    recent_completions = {}
    for record in trainee['completions']:
        training_title = record['name']
        completion_date = datetime.strptime(record['timestamp'], "%m/%d/%Y")

        # Track only the most recent completion date
        if training_title not in recent_completions or recent_completions[training_title]['date'] < completion_date:
            recent_completions[training_title] = {'date': completion_date, 'trainee': trainee['name']}

    # Verify if the completion falls within the specified fiscal year
    for training_title, details in recent_completions.items():
        if training_title in target_trainings and fiscal_start_date <= details['date'] <= fiscal_end_date:
            training_participants[training_title].append(details['trainee'])

# Save output for Task 2
task_2_output_path = output_directory + "output_task_2.json"
with open(task_2_output_path, 'w') as output_file:
    json.dump(training_participants, output_file, indent=4)

# Task 3: Determine trainings that have expired or are due to expire soon
reference_date = datetime(2023, 10, 1)
expiration_threshold = reference_date + timedelta(days=30)

upcoming_expirations = {}
for trainee in training_data:
    expiring_trainings = []
    tracked_trainings = {}

    for record in trainee['completions']:
        training_title = record['name']
        if record['expires']:
            expiry_date = datetime.strptime(record['expires'], "%m/%d/%Y")
            if training_title not in tracked_trainings or tracked_trainings[training_title] < expiry_date:
                tracked_trainings[training_title] = expiry_date

    # Check if training has expired or will expire soon
    for training_title, expiry_date in tracked_trainings.items():
        if expiry_date < reference_date:
            expiring_trainings.append({
                "training_name": training_title,
                "status": "expired"
            })
        elif reference_date <= expiry_date <= expiration_threshold:
            expiring_trainings.append({
                "training_name": training_title,
                "status": "expires soon"
            })

    if expiring_trainings:
        upcoming_expirations[trainee['name']] = expiring_trainings

# Save output for Task 3
task_3_output_path = output_directory + "output_task_3.json"
with open(task_3_output_path, 'w') as output_file:
    json.dump(upcoming_expirations, output_file, indent=4)

print("Results have been successfully saved to the specified directory.")