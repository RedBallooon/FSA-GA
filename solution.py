# import random

# class Solution:
#     def __init__(self, data, schedule=None):
#         self.data = data
#         self.schedule = schedule if schedule else self.generate_random_schedule()
#         self.fitness = self.calculate_fitness()

#     def generate_random_schedule(self):
#         schedule = []
#         days = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]
#         timeslots = ["Sáng", "Trưa", "Chiều"]
#         for entry in self.data.schedule:
#             course_id = entry[0]
#             class_id = entry[1]
#             instructor_id = entry[2]
#             day = random.choice(days)
#             timeslot = random.choice(timeslots)
#             room_id = random.choice(list(self.data.rooms.keys()))
#             schedule.append((course_id, class_id, room_id, day, timeslot))
#         return schedule

#     def calculate_fitness(self):
#         fitness = 0
#         teacher_schedule = {}
#         for entry in self.schedule:
#             course_id, class_id, room_id, day, timeslot = entry
#             instructor_id = self.data.get_teacher_from_course(course_id)
#             if instructor_id is not None:
#                 if (instructor_id, day, timeslot) in teacher_schedule:
#                     fitness += 1
#                 else:
#                     teacher_schedule[(instructor_id, day, timeslot)] = room_id
#         return fitness

#################################################################################################################################################
import random

class Solution:
    def __init__(self, data, schedule=None):
        self.data = data
        if schedule is None:
            self.schedule = self.generate_schedule()
        else:
            self.schedule = schedule
        self.fitness = self.calculate_fitness(self.schedule)

    def generate_schedule(self):
        num_rooms = len(self.data.rooms)
        num_schedule = len(self.data.schedule)  # Kiểm tra độ dài của self.data.schedule
        num_timeslot = 24
        
        schedule = []
        for i in range(num_schedule):
            course_id, _, _ = self.data.schedule[i]  # Đảm bảo self.data.schedule[i] tồn tại và có định dạng đúng
            room_id = random.randint(1, num_rooms)
            timeslot_id = random.randint(1, num_timeslot)
            schedule.append((course_id, room_id, timeslot_id))
        return schedule


    def calculate_fitness(self, schedule):
        fitness = 0
        for i in range(len(schedule)):
            for j in range(i + 1, len(schedule)):
                if self.check_overlap_teaching_schedule(schedule[i], schedule[j]):
                    fitness += 10
                if self.check_duplicate_room(schedule[i], schedule[j]):
                    fitness += 10

            if self.check_room_cap(schedule[i]):
                fitness += 5
            
        return fitness

    def check_overlap_teaching_schedule(self, class1, class2):
        instructor1 = self.data.get_teacher_from_course(class1[0])
        instructor2 = self.data.get_teacher_from_course(class2[0])
        if instructor1 == instructor2 and class1[2] == class2[2]:
            return True
        return False
    
    def check_duplicate_room(self, class1, class2):
        if class1[1] == class2[1] and class1[2] == class2[2]:
            return True
        return False
    
    def check_room_cap(self, course):
        class_id = self.data.get_class_from_course(course[0])
        num_stu = self.data.get_num_students_in_class(class_id)
        room_cap = self.data.get_roomcap(course[1])
        if num_stu and room_cap and num_stu > room_cap:
            return True
        return False
