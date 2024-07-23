import csv
import random
from data import Data
from solution import Solution

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
                # Perform mutation here
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
    
    # Đảm bảo schedule là một đối tượng Solution
    if not isinstance(schedule, Solution):
        raise ValueError("Cần một đối tượng Solution cho lịch học.")

    # Lấy thông tin từ dữ liệu
    classes = schedule.data.classes
    rooms = schedule.data.rooms
    instructors = schedule.data.instructors
    
    # Ràng buộc 1: Sức chứa phòng học
    for entry in schedule.schedule:
        course_id, class_id, room_id, day, timeslot, instructor_id = entry
        class_size = int(classes[class_id]['num_stu'])
        room_capacity = int(rooms[room_id]['cap'])
        if class_size > room_capacity:
            score += 10  # Phạt vi phạm ràng buộc sức chứa phòng học
    
    # Ràng buộc 2: Trùng lịch học
    for i, entry1 in enumerate(schedule.schedule):
        for j, entry2 in enumerate(schedule.schedule):
            if i != j:
                if entry1[2] == entry2[2] and entry1[3] == entry2[3] and entry1[4] == entry2[4]:
                    score += 5  # Phạt trùng lịch học
    
    # Ràng buộc 3: Giáo viên dạy cùng lớp vào cùng thời gian
    for i, entry1 in enumerate(schedule.schedule):
        for j, entry2 in enumerate(schedule.schedule):
            if i != j:
                if entry1[1] == entry2[1] and entry1[3] == entry2[3] and entry1[4] == entry2[4] and entry1[5] == entry2[5]:
                    score += 3  # Phạt trùng giáo viên
    
    # Ràng buộc 4: Giáo viên dạy cùng phòng vào cùng thời gian
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
                    score += (len(teachers) - 1) * 2  # Phạt trùng phòng
    
    # Ưu tiên: Sử dụng hết các phòng có sẵn
    used_rooms = set(entry[2] for entry in schedule.schedule)
    if len(used_rooms) < len(rooms):
        score += (len(rooms) - len(used_rooms)) * 5  # Thưởng sử dụng hết các phòng
    
    return score


def write_schedule_to_csv(file_path, schedule, data):
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['course_id', 'class_id', 'room_id', 'day', 'timeslot', 'instructor_id', 'instructor_name'])
            for entry in schedule:
                course_id, class_id, room_id, day, timeslot, instructor_id = entry
                instructor_name = data.instructors[str(instructor_id)]['name'] if str(instructor_id) in data.instructors else 'Unknown'
                csv_writer.writerow([course_id, class_id, room_id, day, timeslot, instructor_id, instructor_name])
        print(f"Successfully wrote schedule to {file_path}")
    except Exception as e:
        print(f"Error writing schedule to {file_path}: {e}")



class_file = 'class.csv'
instructor_file = 'instructors.csv'
room_file = 'room.csv'
schedule_file = 'schedule.csv'
data = Data(class_file, instructor_file, room_file, schedule_file)

crossover_probability = 0.8
mutation_probability = 0.1
generations = 100
population_size = 50
population = [Solution(data) for _ in range(population_size)]
population.sort(key=lambda x: x.fitness)

for generation in range(generations):
    new_population = []
    for _ in range(population_size // 2):
        parent1, parent2 = random.choices(population[:10], k=2)
        child1 = crossover(parent1, parent2)
        child2 = crossover(parent2, parent1)
        new_population.extend([child1, child2])
    new_population = [mutate(individual, mutation_probability) for individual in new_population]
    new_population.append(population[0])
    population = new_population
    population.sort(key=lambda x: x.fitness)

    print(f"Generation {generation + 1} - Best Fitness: {population[0].fitness}")
    if population[0].fitness == 0:
        break

best_solution = population[0]
print("Best Schedule:")
print(best_solution.schedule)
print("Fitness:", best_solution.fitness)

file_path = 'optimize_1.csv'
write_schedule_to_csv(file_path, best_solution.schedule, data)
