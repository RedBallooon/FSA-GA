document.addEventListener('DOMContentLoaded', function() {
    // Initialize Select2 for teacherSelect
    $('.js-example-basic-single').select2({
        placeholder: 'Chọn giáo viên',
        allowClear: true
    });

    const csvFileInput = document.getElementById('csvFileInput');
    const teacherSelect = document.getElementById('teacherSelect');
    const datePicker = document.getElementById('datePicker');
    const prevWeekBtn = document.getElementById('prevWeekBtn');
    const currentWeekBtn = document.getElementById('currentWeekBtn');
    const nextWeekBtn = document.getElementById('nextWeekBtn');

    const dateMonday = document.getElementById('dateMonday');
    const dateTuesday = document.getElementById('dateTuesday');
    const dateWednesday = document.getElementById('dateWednesday');
    const dateThursday = document.getElementById('dateThursday');
    const dateFriday = document.getElementById('dateFriday');
    const dateSaturday = document.getElementById('dateSaturday');
    const dateSunday = document.getElementById('dateSunday');

    let scheduleData = [];
    let allScheduleData = []; // Store all schedule data for filtering
    let currentWeekStart = getCurrentWeekStartDate();
    let selectedTeacher = ''; // Variable to store selected teacher

    // Add event listeners
    csvFileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            Papa.parse(file, {
                header: true,
                complete: function(results) {
                    allScheduleData = results.data; // Store all schedule data
                    scheduleData = [...allScheduleData]; // Copy all schedule data initially
                    populateTeacherSelect(allScheduleData);
                    displaySchedule();
                }
            });
        }
    });

    // Listen for changes in Select2 dropdown
    $('#teacherSelect').on('select2:select select2:clear', function (e) {
        selectedTeacher = e.params.data.id || ''; // Update selectedTeacher
        filterScheduleByTeacher();
        displaySchedule();
    });

    datePicker.addEventListener('change', function() {
        currentWeekStart = new Date(datePicker.value);
        displaySchedule();
    });

    prevWeekBtn.addEventListener('click', function() {
        changeWeek(-1); // Move to previous week
    });

    currentWeekBtn.addEventListener('click', function() {
        currentWeekStart = getCurrentWeekStartDate(); // Reset to current week
        displaySchedule();
    });

    nextWeekBtn.addEventListener('click', function() {
        changeWeek(1); // Move to next week
    });

    // Function to change week by offset (weeks)
    function changeWeek(offset) {
        currentWeekStart.setDate(currentWeekStart.getDate() + (offset * 7)); // Move by offset weeks
        displaySchedule();
    }

    // Function to populate teacher select options
    function populateTeacherSelect(data) {
        const teachers = new Set(data.map(item => item['instructor_name']));
        const options = Array.from(teachers).map(teacher => ({
            id: teacher,
            text: teacher
        }));
        $('#teacherSelect').select2({
            data: options
        });
    }

    // Function to display schedule based on selected teacher and current week
    function displaySchedule() {
        const startDate = new Date(currentWeekStart);

        dateMonday.textContent = formatDate(startDate);
        dateTuesday.textContent = formatDate(addDays(startDate, 1));
        dateWednesday.textContent = formatDate(addDays(startDate, 2));
        dateThursday.textContent = formatDate(addDays(startDate, 3));
        dateFriday.textContent = formatDate(addDays(startDate, 4));
        dateSaturday.textContent = formatDate(addDays(startDate, 5));
        dateSunday.textContent = formatDate(addDays(startDate, 6));

        const cells = document.querySelectorAll('.cell');
        cells.forEach(cell => {
            cell.classList.remove('occupied');
            cell.innerHTML = '';
        });

        scheduleData.forEach(item => {
            const dayIndex = getDayIndex(item['day']);
            const timeslot = item['timeslot'];
            const instructor = item['instructor_name'];

            const cell = document.querySelector(`.cell[data-day="${dayIndex}"][data-slot="${timeslot}"]`);
            if (cell && (selectedTeacher === '' || instructor === selectedTeacher)) {
                const info = `Mã Học Phần: ${item['course_id']}<br>Mã Lớp: ${item['class_id']}<br>Mã Phòng: ${item['room_id']}<br>Giảng Viên: ${instructor}`;
                cell.innerHTML = info;
                cell.classList.add('occupied');
            }
        });
    }

    // Function to filter schedule data by selected teacher
    function filterScheduleByTeacher() {
        if (selectedTeacher === '') {
            scheduleData = [...allScheduleData]; // Restore original data
        } else {
            scheduleData = allScheduleData.filter(item => item['instructor_name'] === selectedTeacher);
        }
    }

    // Function to format date as DD/MM/YYYY
    function formatDate(date) {
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        return `${day}/${month}/${year}`;
    }

    // Function to add days to a date
    function addDays(date, days) {
        const result = new Date(date);
        result.setDate(result.getDate() + days);
        return result;
    }

    // Function to get day index (2 for Monday, 3 for Tuesday, ...)
    function getDayIndex(dayName) {
        switch (dayName) {
            case 'Thứ 2':
                return 2;
            case 'Thứ 3':
                return 3;
            case 'Thứ 4':
                return 4;
            case 'Thứ 5':
                return 5;
            case 'Thứ 6':
                return 6;
            case 'Thứ 7':
                return 7;
            case 'Chủ nhật':
                return 8;
            default:
                return -1;
        }
    }

    // Function to get the start date of the current week
    function getCurrentWeekStartDate() {
        const currentDate = new Date();
        const currentDay = currentDate.getDay();
        const diff = currentDate.getDate() - currentDay + (currentDay === 0 ? -6 : 1); // Adjust when currentDay is Sunday (0)
        const weekStart = new Date(currentDate.setDate(diff));
        return weekStart;
    }

    // Initial display for current week
    displaySchedule();
});
