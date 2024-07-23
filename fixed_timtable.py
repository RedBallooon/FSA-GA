import csv
import random
import math

class Data:
    def __init__(self, class_file, instructor_file, room_file, schedule_file=None):
        self.classes = self.load_csv(class_file, 'class_id')
        self.instructors = self.load_csv(instructor_file, 'instructor_id')
        self.rooms = self.load_csv(room_file, 'room_id')
        self.schedule = self.load_csv(schedule_file, 'schedule_id') if schedule_file else []

    def load_csv(self, file_path, id_field):
        data = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    key = int(row[id_field])
                    data[key] = row
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error loading CSV file {file_path}: {e}")
        return data

class Solution:
    def __init__(self, data, schedule=None):
        self.data = data
        self.schedule = schedule if schedule else self.generate_initial_schedule()
        self.fitness = self.calculate_fitness()

    def generate_initial_schedule(self):
        days = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]
        timeslots = ["Sáng", "Trưa", "Chiều"]
        schedule = []
        used_slots = set()
        
        for class_id in self.data.classes:
            course_id = self.data.classes[class_id]['course_id']
            room_id = random.choice(list(self.data.rooms.keys()))
            day = random.choice(days)
            timeslot = random.choice(timeslots)
            instructor_id = random.choice(list(self.data.instructors.keys()))
            slot = (course_id, class_id, room_id, day, timeslot, instructor_id)
            
            # Kiểm tra xung đột phòng và giáo viên
            while (slot[2], slot[3], slot[4]) in used_slots or any(slot[5] == other[5] for other in schedule if other[2] == slot[2] and other[3] == slot[3] and other[4] == slot[4]):
                room_id = random.choice(list(self.data.rooms.keys()))
                day = random.choice(days)
                timeslot = random.choice(timeslots)
                instructor_id = random.choice(list(self.data.instructors.keys()))
                slot = (course_id, class_id, room_id, day, timeslot, instructor_id)
            
            used_slots.add((room_id, day, timeslot))
            schedule.append(slot)
        
        return schedule

    def calculate_fitness(self):
        score = 0
        schedule_set = set()
        room_conflicts = {}
        teacher_conflicts = {}
        
        for entry in self.schedule:
            if entry in schedule_set:
                score += 10  # Phạt trùng lịch học
            schedule_set.add(entry)
            
            course_id, class_id, room_id, day, timeslot, instructor_id = entry
            
            if (day, timeslot, room_id) not in room_conflicts:
                room_conflicts[(day, timeslot, room_id)] = []
            room_conflicts[(day, timeslot, room_id)].append(class_id)
            
            if (day, timeslot, instructor_id) not in teacher_conflicts:
                teacher_conflicts[(day, timeslot, instructor_id)] = []
            teacher_conflicts[(day, timeslot, instructor_id)].append(class_id)
        
        for key, conflicts in room_conflicts.items():
            if len(conflicts) > 1:
                score += (len(conflicts) - 1) * 2  # Phạt trùng phòng
        
        for key, conflicts in teacher_conflicts.items():
            if len(conflicts) > 1:
                score += (len(conflicts) - 1) * 2  # Phạt trùng giáo viên

        used_rooms = set(entry[2] for entry in self.schedule)
        if len(used_rooms) < len(self.data.rooms):
            score += (len(self.data.rooms) - len(used_rooms)) * 5  # Thưởng sử dụng hết các phòng
        
        return score

def crossover(parent1, parent2):
    crossover_point = random.randint(0, min(len(parent1.schedule), len(parent2.schedule)) - 1)
    child_schedule = parent1.schedule[:crossover_point] + parent2.schedule[crossover_point:]
    return Solution(parent1.data, child_schedule)

def mutate(individual, mutation_rate=0.1):
    days = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]
    timeslots = ["Sáng", "Trưa", "Chiều"]
    num_rooms = len(individual.data.rooms)
    num_instructors = len(individual.data.instructors)
    num_schedule = len(individual.schedule)
    mutated_schedule = []
    used_slots = set()
    
    for i in range(num_schedule):
        if random.random() > mutation_rate:
            mutated_schedule.append(individual.schedule[i])
            used_slots.add(individual.schedule[i])
        else:
            course_id, class_id, room_id, day, timeslot, instructor_id = individual.schedule[i]
            room_id = random.choice(list(individual.data.rooms.keys()))
            day = random.choice(days)
            timeslot = random.choice(timeslots)
            instructor_id = random.choice(list(individual.data.instructors.keys()))
            new_slot = (course_id, class_id, room_id, day, timeslot, instructor_id)
            
            # Kiểm tra xung đột
            while new_slot in used_slots or any(new_slot[2] == other[2] and new_slot[3] == other[3] and new_slot[4] == other[4] and new_slot[5] == other[5] for other in mutated_schedule):
                room_id = random.choice(list(individual.data.rooms.keys()))
                day = random.choice(days)
                timeslot = random.choice(timeslots)
                instructor_id = random.choice(list(individual.data.instructors.keys()))
                new_slot = (course_id, class_id, room_id, day, timeslot, instructor_id)
            
            used_slots.add(new_slot)
            mutated_schedule.append(new_slot)
    
    return Solution(individual.data, mutated_schedule)

def flamingo_search_algorithm(data, population_size=50, generations=1000, mutation_rate=0.1):
    # Initialize population
    population = [Solution(data) for _ in range(population_size)]
    population.sort(key=lambda x: x.fitness)

    # FSA parameters
    alpha = 0.5  # Relative importance of exploration vs. exploitation
    beta = 0.5   # Relative importance of the individual vs. the group

    for generation in range(generations):
        # FSA update
        new_population = []
        for i in range(population_size):
            # Flamingo search
            leader = random.choice(population[:10])
            new_schedule = leader.schedule[:]
            for _ in range(random.randint(1, len(new_schedule))):
                index = random.randint(0, len(new_schedule) - 1)
                new_schedule[index] = (random.choice(list(data.classes.keys())),
                                       new_schedule[index][1], 
                                       random.choice(list(data.rooms.keys())),
                                       random.choice(["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]),
                                       random.choice(["Sáng", "Trưa", "Chiều"]),
                                       random.choice(list(data.instructors.keys())))
            new_population.append(Solution(data, new_schedule))
        
        # Evaluate new population
        population.extend(new_population)
        population = sorted(population, key=lambda x: x.fitness)[:population_size]

        print(f"Generation {generation + 1} - Best Fitness: {population[0].fitness}")
        if population[0].fitness == 0:
            print("Optimal schedule found.")
            break

    best_solution = population[0]
    print("Best Schedule:")
    for entry in best_solution.schedule:
        course_id, class_id, room_id, day, timeslot, instructor_id = entry
        instructor_name = data.instructors.get(instructor_id, {}).get('fullname', 'Unknown')
        print(f"Course ID: {course_id}, Class ID: {class_id}, Room ID: {room_id}, Day: {day}, Timeslot: {timeslot}, Instructor ID: {instructor_id}, Instructor Name: {instructor_name}")
    print("Fitness:", best_solution.fitness)

    return best_solution

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

# Main execution
def main():
    class_file = 'classes.csv'
    instructor_file = 'instructors.csv'
    room_file = 'rooms.csv'
    schedule_file = None  # Nếu bạn không có file schedule ban đầu

    data = Data(class_file, instructor_file, room_file, schedule_file)

    best_solution = flamingo_search_algorithm(data)

    file_path = 'optimized_schedule.csv'
    write_schedule_to_csv(file_path, best_solution.schedule, data)

if __name__ == "__main__":
    main()
