import csv
from collections import defaultdict

# Đọc dữ liệu từ file CSV
def read_schedule(file_path):
    schedule = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Bỏ qua dòng tiêu đề
        for row in csv_reader:
            schedule.append(tuple(row))
    return schedule

# Kiểm tra sự trùng lặp
def check_for_duplicates(schedule):
    room_time = defaultdict(list)
    teacher_time = defaultdict(list)
    course_class_time = defaultdict(list)
    
    for entry in schedule:
        course_id, class_id, room_id, day, timeslot, instructor_id, instructor_name = entry
        room_time[(day, timeslot)].append(room_id)
        teacher_time[(day, timeslot)].append(instructor_id)
        course_class_time[(day, timeslot, room_id)].append((course_id, class_id, instructor_id))
        
    duplicates = {'rooms': [], 'teachers': [], 'courses': []}
    for key, rooms in room_time.items():
        if len(set(rooms)) < len(rooms):
            duplicates['rooms'].append((key, rooms))
    
    for key, teachers in teacher_time.items():
        if len(set(teachers)) < len(teachers):
            duplicates['teachers'].append((key, teachers))
    
    for key, classes in course_class_time.items():
        seen = set()
        for course_class in classes:
            if course_class in seen:
                duplicates['courses'].append((key, classes))
                break
            seen.add(course_class)
    
    return duplicates

# Đọc và kiểm tra lịch trình
schedule = read_schedule('optimized_schedule.csv')
duplicates = check_for_duplicates(schedule)

if duplicates['rooms']:
    print("Room conflicts found:")
    for conflict in duplicates['rooms']:
        print(f"Day: {conflict[0][0]}, Timeslot: {conflict[0][1]}, Rooms: {conflict[1]}")

if duplicates['teachers']:
    print("Teacher conflicts found:")
    for conflict in duplicates['teachers']:
        print(f"Day: {conflict[0][0]}, Timeslot: {conflict[0][1]}, Teachers: {conflict[1]}")

if duplicates['courses']:
    print("Course conflicts found:")
    for conflict in duplicates['courses']:
        print(f"Day: {conflict[0][0]}, Timeslot: {conflict[0][1]}, Room: {conflict[0][2]}, Conflicting courses/classes: {conflict[1]}")

if not duplicates['rooms'] and not duplicates['teachers'] and not duplicates['courses']:
    print("No conflicts found.")
