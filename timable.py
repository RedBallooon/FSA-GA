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
    num_schedule = len(individual.schedule)
    mutated_schedule = []
    for i in range(num_schedule):
        if random.random() > mutation_rate:
            mutated_schedule.append(individual.schedule[i])
        else:
            course_id, class_id, room_id, day, timeslot = individual.schedule[i]
            room_id = random.randint(1, num_rooms)
            day = random.choice(days)
            timeslot = random.choice(timeslots)
            mutated_schedule.append((course_id, class_id, room_id, day, timeslot))

    return Solution(individual.data, mutated_schedule)

def write_schedule_to_csv(file_path, schedule):
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['course_id', 'class_id', 'room_id', 'day', 'timeslot'])
            for entry in schedule:
                csv_writer.writerow(entry)
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
write_schedule_to_csv(file_path, best_solution.schedule)