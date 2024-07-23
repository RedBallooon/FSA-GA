import csv

class Data:
    def __init__(self, class_file, instructor_file, room_file):
        self.classes = self.load_classes(class_file)
        self.instructors = self.load_instructors(instructor_file)
        self.rooms = self.load_rooms(room_file)

    def load_classes(self, file_path):
        classes = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                class_id = int(row['class_id'])
                classes[class_id] = {
                    'course_id': int(row['course_id']),
                    'num': int(row['num'])
                }
        return classes

    def load_instructors(self, file_path):
        instructors = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                instructor_id = int(row['instructor_id'])
                instructors[instructor_id] = {
                    'fullname': row['fullname'],
                    'degree': row['degree'],
                    'department': row['department']
                }
        return instructors

    def load_rooms(self, file_path):
        rooms = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                room_id = int(row['room_id'])
                rooms[room_id] = {
                    'name': row['name'],
                    'type': row['type'],
                    'capacity': int(row['capacity'])
                }
        return rooms
