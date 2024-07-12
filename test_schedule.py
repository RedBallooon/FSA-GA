# import numpy as np
# import random
# from data import Data
# from solution import Solution
# from FSA_GA import flamingo_search, genetic_algorithm, flamingo_genetic_search

# # Hàm mục tiêu
# def objective_function(schedule):
#     score = 0
    
#     # Đảm bảo schedule là một đối tượng Solution
#     if not isinstance(schedule, Solution):
#         raise ValueError("Cần một đối tượng Solution cho lịch học.")

#     # Lấy thông tin từ dữ liệu
#     classes = schedule.data.classes
#     rooms = schedule.data.rooms
#     instructors = schedule.data.instructors
    
#     # Ràng buộc 1: Sức chứa phòng học
#     for entry in schedule.schedule:
#         course_id, class_id, room_id, day, timeslot = entry
#         class_size = int(classes[class_id]['num_stu'])
#         room_capacity = int(rooms[room_id]['cap'])
#         if class_size > room_capacity:
#             score += 10  # Phạt vi phạm ràng buộc sức chứa phòng học
    
#     # Ràng buộc 2: Trùng lịch học
#     for i, entry1 in enumerate(schedule.schedule):
#         for j, entry2 in enumerate(schedule.schedule):
#             if i != j:
#                 if entry1[2] == entry2[2] and entry1[3] == entry2[3] and entry1[4] == entry2[4]:
#                     score += 5  # Phạt trùng lịch học
    
#     # Ràng buộc 3: Giáo viên dạy cùng lớp vào cùng thời gian
#     for i, entry1 in enumerate(schedule.schedule):
#         for j, entry2 in enumerate(schedule.schedule):
#             if i != j:
#                 if entry1[1] == entry2[1] and entry1[3] == entry2[3] and entry1[4] == entry2[4]:
#                     score += 3  # Phạt trùng giáo viên
    
#     # Ràng buộc 4: Giáo viên dạy cùng phòng vào cùng thời gian
#     for day in ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]:
#         for timeslot in ["Sáng", "Trưa", "Chiều"]:
#             teachers_in_timeslot = {}
#             for entry in schedule.schedule:
#                 course_id, class_id, room_id, day_entry, timeslot_entry = entry
#                 if day_entry == day and timeslot_entry == timeslot:
#                     if room_id not in teachers_in_timeslot:
#                         teachers_in_timeslot[room_id] = set()
#                     teachers_in_timeslot[room_id].add(class_id)
            
#             for room_id, teachers in teachers_in_timeslot.items():
#                 if len(teachers) > 1:
#                     score += (len(teachers) - 1) * 2  # Phạt trùng phòng
    
#     # Ưu tiên: Sử dụng hết các phòng có sẵn
#     used_rooms = set(entry[2] for entry in schedule.schedule)
#     if len(used_rooms) < len(rooms):
#         score += (len(rooms) - len(used_rooms)) * 5  # Thưởng sử dụng hết các phòng
    
#     return score


# # Hàm ghi ra file CSV
# def write_schedule_to_csv(file_path, schedule):
#     try:
#         with open(file_path, 'w', newline='', encoding='utf-8') as file:
#             csv_writer = csv.writer(file)
#             csv_writer.writerow(['course_id', 'class_id', 'room_id', 'day', 'timeslot'])
#             for entry in schedule:
#                 csv_writer.writerow(entry)
#         print(f"Ghi lịch học thành công vào {file_path}")
#     except Exception as e:
#         print(f"Lỗi khi ghi lịch học vào {file_path}: {e}")


# # Chương trình chính cho quá trình tối ưu

# class_file = 'class.csv'
# instructor_file = 'instructors.csv'
# room_file = 'room.csv'
# schedule_file = 'schedule.csv'

# # Khởi tạo đối tượng Data
# data = Data(class_file, instructor_file, room_file, schedule_file)

# # Tham số cho thuật toán Flamingo Search
# initial_solution = []  # Giải pháp ban đầu cho Flamingo Search
# n_iter = 100  # Số lần lặp cho Flamingo Search
# n_flamingos = 10  # Số lượng flamingo trong mỗi lần lặp
# sigma = 0.1  # Tham số cho thuật toán Flamingo Search

# # Tham số cho thuật toán Genetic Algorithm
# population_size = 50
# generations = 100
# mutation_rate = 0.1
# elitism_rate = 0.1

# # Thực hiện Flamingo Search để tìm giải pháp ban đầu
# try:
#     initial_solution, _ = flamingo_search(objective_function, initial_solution, n_iter, n_flamingos, sigma)
    
#     # Khởi tạo quần thể cho Genetic Algorithm
#     population = np.random.uniform(-5, 5, (population_size, len(initial_solution)))
#     population[0] = initial_solution  # Đặt cá thể đầu tiên là giải pháp tốt nhất từ Flamingo Search
    
#     # Thực hiện Genetic Algorithm để tối ưu hóa lịch học
#     best_solution, convergence = genetic_algorithm(population, objective_function, generations, mutation_rate, elitism_rate)
    
#     # In ra lịch học tốt nhất và giá trị fitness
#     print("Lịch học tốt nhất:")
#     print(best_solution)
#     print("Giá trị fitness:", objective_function(best_solution))
    
#     # Ghi lịch học tốt nhất ra file CSV
#     file_path = 'optimized_schedule.csv'
#     write_schedule_to_csv(file_path, best_solution)

# except ValueError as e:
#     print(f"Lỗi trong quá trình tối ưu hóa: {e}")

#####################################################################################################################################################################################


import pandas as pd
from FSA_GA import Solution, flamingo_genetic_search

# Hàm mục tiêu
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
        course_id, class_id, room_id, day, timeslot = entry
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
                if entry1[1] == entry2[1] and entry1[3] == entry2[3] and entry1[4] == entry2[4]:
                    score += 3  # Phạt trùng giáo viên
    
    # Ràng buộc 4: Giáo viên dạy cùng phòng vào cùng thời gian
    for day in ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]:
        for timeslot in ["Sáng", "Trưa", "Chiều"]:
            teachers_in_timeslot = {}
            for entry in schedule.schedule:
                course_id, class_id, room_id, day_entry, timeslot_entry = entry
                if day_entry == day and timeslot_entry == timeslot:
                    if room_id not in teachers_in_timeslot:
                        teachers_in_timeslot[room_id] = set()
                    teachers_in_timeslot[room_id].add(class_id)
            
            for room_id, teachers in teachers_in_timeslot.items():
                if len(teachers) > 1:
                    score += (len(teachers) - 1) * 2  # Phạt trùng phòng
    
    # Ưu tiên: Sử dụng hết các phòng có sẵn
    used_rooms = set(entry[2] for entry in schedule.schedule)
    if len(used_rooms) < len(rooms):
        score += (len(rooms) - len(used_rooms)) * 5  # Thưởng sử dụng hết các phòng
    
    return score

# Đọc dữ liệu từ các file CSV
class_file = 'class.csv'
instructor_file = 'instructors.csv'
room_file = 'room.csv'
schedule_file = 'schedule.csv'

class_data = pd.read_csv(class_file)
instructor_data = pd.read_csv(instructor_file)
room_data = pd.read_csv(room_file)
schedule_data = pd.read_csv(schedule_file)

# Khởi tạo đối tượng Solution từ dữ liệu
solution = Solution(class_data, instructor_data, room_data, schedule_data)

# Thực hiện tối ưu hóa lịch học bằng Flamingo Search và Genetic Algorithm
try:
    n_iter = 100  # Số lần lặp của Flamingo Search
    n_flamingos = 10  # Số lượng "flamingos" (giải pháp ngẫu nhiên) trong mỗi lần lặp
    sigma = 0.1  # Độ lệch chuẩn của phân phối normal trong Flamingo Search
    generations = 100  # Số thế hệ của Genetic Algorithm
    population_size = 50  # Kích thước quần thể trong Genetic Algorithm

    # Thực hiện tối ưu hóa lịch học
    best_solution, convergence = flamingo_genetic_search(objective_function, solution, n_iter, n_flamingos, sigma, generations, population_size)

    # In ra lịch học tối ưu và giá trị fitness tương ứng
    print("Lịch học tối ưu:")
    print(best_solution.schedule)
    print("Giá trị fitness:", objective_function(best_solution.schedule))

    # Ghi lịch học tối ưu ra file CSV nếu cần
    # file_path = 'optimized_schedule.csv'
    # write_schedule_to_csv(file_path, best_solution.schedule)

except ValueError as e:
    print(f"Lỗi trong quá trình tối ưu hóa: {e}")
