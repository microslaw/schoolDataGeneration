classroom_count = 357  # How many classrooms are there in the school
teacher_count = 300  # How many teachers work in the school
course_count = 300  # How many courses are there in the school
class_count = 10  # How many classes per year are there in the school; If max_school_years = 6, will generate 60 classes
student_count = 800  # How many students are there in the school

# Count's of tuples below are determined by different parameters. Setting count other than 0, will cutoff remaining tuples
# This may break the integrity of the data
meeting_count = 0  # normal value: course_count * classes_count * number of school days between start_date and end_date
exam_count = 0 # total number of school monhs between start_date and end_date * student_count * course_per_class_count
survey_count = 0  # total number of school monhs between start_date and end_date * student_count
attendance_count = 0 # mostly random, heavily depends on the attendanceProb parameter


classroom_max_number = 999
classroom_max_floors = 8
classroom_min_max_capacity = 25
classroom_max_max_capacity = 40

teacher_min_age = 25
teacher_max_age = 65

max_school_years = 6
course_per_class_count = 7

# present_year

student_min_age = 10
# students_max_age is calculated as: students_min_age + max_school_years

school_start_hour = 7
school_end_hour = 19

exam_min_score = 0
exam_max_score = 50
exam_resolution = 1/4

survey_min_score = 0
survey_max_score = 20
survey_resolution = 1/4

excused_prob = 0.7
late_prob = 0.2
attendance_prob = 0.99

start_date = "2020-06-20"
end_date = "2020-09-10"


default_city_districts = [
    "Wejherowo",
    "Redlowo",
    "Orlowo",
    "Reda",
    "Gdynia centrum",
    "Gdansk centrum",
    "Zaspa",
    "Jasien",
    "Orunia",
    "Przymorze",
    "Wrzeszcz",
    "Stocznia",
    "Lostowice",
]


default_city_districts_trend_dict = {
    "Wejherowo": 70,
    "Redlowo": 40,
    "Orlowo": 35,
    "Reda": 55,
    "Gdynia centrum": 50,
    "Gdansk centrum": 20,
    "Zaspa": 20,
    "Jasien": 40,
    "Orunia": 30,
    "Przymorze": 25,
    "Wrzeszcz": 15,
    "Stocznia": 10,
    "Lostowice": 60,
}


default_specializations = {
    "Mathematical": ["Mathematics", "Physics", "Informatics"],
    "Humanistic": ["Polish", "Psychology", "History"],
    "Scientific": ["Biology", "Chemistry", "Physics"],
    "Linguistic": ["English", "German", "French"],
    "Artistic": ["Art", "Music", "History"],
    "Sport": ["PE", "Biology", "Physics"],
}


default_course_names = [
    "Mathematics",
    "Polish",
    "English",
    "Physics",
    "Chemistry",
    "Biology",
    "History",
    "Geography",
    "PE",
    "Art",
    "Music",
    "Informatics",
    "Religion",
    "Ethics",
    "Psychology",
    "Sociology",
    "Philosophy",
    "Economics",
    "German",
    "French",
]

default_catchup_tasks = [
    "Read pages 1-10",
    "Do exercises 1-5",
    "Read pages 11-20",
    "Do exercises 6-10",
    "Read pages 21-30",
    "Do exercises 11-15",
    "Read pages 31-40",
    "Do entire page 41",
    "Do tasks 5 and 7a from page 42",
    "Write a summary of the chapter",
    "None",
]

# specialization/course check
for key, value in default_specializations.items():
    for course in value:
        if course not in default_course_names:
            raise ValueError(f"Course {course} is not in defaultCourseNames")


# cityDistricts check
for district in default_city_districts:
    if district not in default_city_districts_trend_dict.keys():
        raise ValueError(f"District {district} is not in defaultCityDistrictsTrendDict")
