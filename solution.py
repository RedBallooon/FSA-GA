import random
from data import Data

class Solution:
    def __init__(self, data, schedule=None):
        self.data = data
        self.schedule = schedule if schedule else self.generate_initial_schedule()
        self.fitness = self.calculate_fitness()

    def generate_initial_schedule(self):
        days = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]
        timeslots = ["Sáng", "Trưa", "Chiều"]
        schedule = []
        for class_id in self.data.classes:
            course_id = self.data.classes[class_id]['course_id']
            room_id = random.choice(list(self.data.rooms.keys()))
            day = random.choice(days)
            timeslot = random.choice(timeslots)
            instructor_id = random.choice(list(self.data.instructors.keys()))
            schedule.append((course_id, class_id, room_id, day, timeslot, instructor_id))
        return schedule

    def calculate_fitness(self):
        return objective_function(self)

def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1.schedule) - 1)
    child_schedule = parent1.schedule[:crossover_point] + parent2.schedule[crossover_point:]
    return Solution(parent1.data, child_schedule)

def mutate(individual, mutation_rate=0.1):
    days = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]
    timeslots = ["Sáng", "Trưa", "Chiều"]
    num_rooms = len(individual.data.rooms)
    num_instructors = len(individual.data.instructors)
    num_schedule = len(individual.schedule)
    mutated_schedule = []
    for i in range(num_schedule):
        if random.random() > mutation_rate:
            mutated_schedule.append(individual.schedule[i])
        else:
            try:
                course_id, class_id, room_id, day, timeslot, instructor_id = individual.schedule[i]
                room_id = random.randint(1, num_rooms)
                day = random.choice(days)
                timeslot = random.choice(timeslots)
                instructor_id = random.choice(list(individual.data.instructors.keys()))
                mutated_schedule.append((course_id, class_id, room_id, day, timeslot, instructor_id))
            except ValueError as e:
                print(f"Error mutating schedule at index {i}: {e}")
                print(f"Problematic entry: {individual.schedule[i]}")
                raise  # Raise the error to halt execution and debug further

    return Solution(individual.data, mutated_schedule)

def objective_function(schedule):
    score = 0
    
    if not isinstance(schedule, Solution):
        raise ValueError("Cần một đối tượng Solution cho lịch học.")

    classes = schedule.data.classes
    rooms = schedule.data.rooms
    instructors = schedule.data.instructors
    
    for entry in schedule.schedule:
        course_id, class_id, room_id, day, timeslot, instructor_id = entry
        class_size = int(classes[class_id]['num'])
        room_capacity = int(rooms[room_id]['capacity'])
        if class_size > room_capacity:
            score += 10
    
    for i, entry1 in enumerate(schedule.schedule):
        for j, entry2 in enumerate(schedule.schedule):
            if i != j:
                if entry1[2] == entry2[2] and entry1[3] == entry2[3] and entry1[4] == entry2[4]:
                    score += 5
    
    for i, entry1 in enumerate(schedule.schedule):
        for j, entry2 in enumerate(schedule.schedule):
            if i != j:
                if entry1[1] == entry2[1] and entry1[3] == entry2[3] and entry1[4] == entry2[4] and entry1[5] == entry2[5]:
                    score += 3
    
    for day in ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]:
        for timeslot in ["Sáng", "Trưa", "Chiều"]:
            teachers_in_timeslot = {}
            for entry in schedule.schedule:
                course_id, class_id, room_id, day_entry, timeslot_entry, instructor_id = entry
                if day_entry == day and timeslot_entry == timeslot:
                    if room_id not in teachers_in_timeslot:
                        teachers_in_timeslot[room_id] = set()
                    teachers_in_timeslot[room_id].add(instructor_id)
            
            for room_id, teachers in teachers_in_timeslot.items():
                if len(teachers) > 1:
                    score += (len(teachers) - 1) * 2
    
    used_rooms = set(entry[2] for entry in schedule.schedule)
    if len(used_rooms) < len(rooms):
        score += (len(rooms) - len(used_rooms)) * 5
    
    return score

def write_schedule_to_csv(file_path, schedule, data):
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['course_id', 'class_id', 'room_id', 'day', 'timeslot', 'instructor_id', 'instructor_name'])
            for entry in schedule:
                course_id, class_id, room_id, day, timeslot, instructor_id = entry
                instructor_name = data.instructors[instructor_id]['fullname'] if instructor_id in data.instructors else 'Unknown'
                csv_writer.writerow([course_id, class_id, room_id, day, timeslot, instructor_id, instructor_name])
        print(f"Successfully wrote schedule to {file_path}")
    except Exception as e:
        print(f"Error writing schedule to {file_path}: {e}")
