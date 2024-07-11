import csv

class Data:
    def __init__(self, class_file, instructor_file, room_file, schedule_file):
        self.classes = self.load_classes(class_file)
        self.instructors = self.load_instructors(instructor_file)
        self.rooms = self.load_rooms(room_file)
        self.schedule = self.load_schedule(schedule_file)

    def load_classes(self, class_file):
        classes = {}
        with open(class_file, 'r', encoding='utf-8') as file:
            next(file)  # skip header
            for line in file:
                id, class_name, num_students = line.strip().split(',')
                classes[int(id)] = (class_name, int(num_students))
        return classes

    def load_instructors(self, instructor_file):
        instructors = {}
        with open(instructor_file, 'r', encoding='utf-8') as file:
            next(file)  # skip header
            for line in file:
                if line.strip():  # Check if line is not empty
                    id, name = line.strip().split(',')
                    instructors[int(id)] = name
        return instructors

    def load_rooms(self, room_file):
        rooms = {}
        with open(room_file, 'r', encoding='utf-8') as file:
            next(file)  # skip header
            for line in file:
                id, room, cap = line.strip().split(',')
                rooms[int(id)] = (room, int(cap))
        return rooms

    def load_schedule(self, schedule_file):
        schedule = []
        try:
            with open(schedule_file, 'r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip header
                for row in csv_reader:
                    course_id = int(row[0])
                    class_id = int(row[2])
                    instructor_id = int(row[3])
                    entry = (course_id, class_id, instructor_id)
                    schedule.append(entry)
            print(f"Successfully read schedule from {schedule_file}")
        except Exception as e:
            print(f"Error reading schedule from {schedule_file}: {e}")

        return schedule

    def get_teacher_from_course(self, course_id):
        for entry in self.schedule:
            if entry[0] == course_id:
                return entry[2]
        return None

    def get_class_from_course(self, course_id):
        for entry in self.schedule:
            if entry[0] == course_id:
                return entry[1]
        return None

    def get_num_students_in_class(self, class_id):
        for key, value in self.classes.items():
            if key == class_id:
                return value[1]
        return None

    def get_roomcap(self, room_id):
        for key, value in self.rooms.items():
            if key == room_id:
                return value[1]
        return None

    
# # Tạo đối tượng Data từ các file dữ liệu của bạn
# class_file = 'class.csv'
# instructor_file = 'instructors.csv'
# room_file = 'room.csv'
# schedule_file = 'schedule.csv'

# data = Data(class_file, instructor_file, room_file, schedule_file)

# # In ra thông tin từ các file đã đọc được
# print("Classes:")
# print(data.classes)
# print()

# print("Instructors:")
# print(data.instructors)
# print()

# print("Rooms:")
# print(data.rooms)
# print()

# print("Schedule:")
# print(data.schedule)
# print()
