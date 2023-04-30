from django.db import models

# Create your models here.

class Semester(models.Model):
    year = models.PositiveIntegerField()
    semester_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('year', 'semester_number',)
        ordering = ('-year', '-semester_number',)

    def __str__(self):
        return f"{self.get_semester_display()} {self.year}"

    def get_semester_display(self):
        if self.semester_number == 1:
            return "1st Semester"
        elif self.semester_number == 2:
            return "2nd Semester"
        elif self.semester_number == 3:
            return "Summer Term"
        else:
            return f"{self.semester_number}th Semester"


class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=100)
    semesters = models.ManyToManyField('Semester')

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

class Lecturer(models.Model):
    staff_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    courses = models.ManyToManyField('Course')
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.staff_number})"

class Class(models.Model):
    class_number = models.CharField(max_length=20)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Class {self.class_number} ({self.course.course_code}, " \
               f"{self.semester.year} {self.semester.semester_number})"
class Student(models.Model):
    student_number = models.PositiveIntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Student: {self.first_name} {self.last_name}'


class StudentEnrollment(models.Model):
    student_number = models.ForeignKey('Student', on_delete=models.CASCADE)
    class_enrolled = models.ForeignKey('Class', on_delete=models.CASCADE)
    grade = models.PositiveIntegerField()
    enroll_time = models.DateTimeField(auto_now_add=True)
    grade_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student_number} - {self.class_enrolled} - Grade: {self.grade}"


