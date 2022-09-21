"""
@author : <ihitiman>
@date: October 12, 2021
 
Description: A grade book maintains a record of scores that 
students have in all courses that they have registered for.
"""
from course import Course  
class GradeBook:
    
    def __init__(self):
        self.__courses={}
        
    # Accessor
    def getCourses(self):
        return self.__courses

    def find(self,rollNum):
        """
        A method that receives a student’s roll number and returns true if
        the student exists in the grade book. It returns false, otherwise.
        """
        if_existing = 0
        available_courses= self.__courses
        for course in available_courses:
            for enrolled in available_courses[course].getClasslist(): 
                if rollNum == enrolled.getRollNum():
                    if_existing = 1
        if(if_existing==1):
            return True
        else:
            return False

    def readCourses(self):
        """reads and store course filenames in a list"""
        couseList = [couseList for couseList in input("Enter comma-separated course filenames: ").split(",")]
        #print(f"Courses list: {couseList}")
        for filename in couseList:
            course = Course()
            course.addCourseDataFromFile(filename)
            course.addStudentsFromFile(filename)
            self.__courses[course.getCourseID()] = course
    
    def passedAllCourses(self):
        """
        A method that generate a file (passes.txt) to show the list of
        all students who have passed all registered course
        """
        filewriter= open("passes.txt", 'w')
        students_passed = []
        for course in self.__courses.values():
            for student in course.getClasslist():
                if student.percentageGen() < 40 :
                    continue
                students_passed.append([student.getRollNum(),student.getName()])
        students_passed_all_courses=[]
        for student in students_passed:
            if(students_passed.count(student)==5):
                if student in students_passed_all_courses:
                    continue
                students_passed_all_courses.append(student)  
        students_passed_all_courses.sort(key = lambda x: x[0])
        for student in students_passed_all_courses:
            filewriter.write(f"{student[0]}\t\t\t{student[1]}\t\t\t\n")
        filewriter.close()
    
    def failedStudents(self):
        """
        A method that generates a file (referrals.txt) to shows the list of
        all students who have referrals
        """
        filewriter= open("referrals.txt", 'w')
        referrals = []
        failed_students = []
        for course in self.__courses.values():
            for student in course.getClasslist():
                if student.percentageGen() >= 40 :
                    continue
                referrals.append([student.getRollNum(),student.getName(),course.getCourseName()])
                if [student.getRollNum(),student.getName()] in failed_students:
                    continue
                failed_students.append([student.getRollNum(),student.getName()])
        
        failed_students.sort(key = lambda x: x[0])
        for student in failed_students:
            filewriter.write(f"{student[0]}\t\t\t\t{student[1]}\t\t\t\t") 
            for referred_student in referrals:
                if referred_student[0]!=student[0]:
                    continue
                filewriter.write(f"\n\t\t{referred_student[2]}\n")
        filewriter.close()

    def studentsGrade(self):
        """
        A method to generate a file (grades.txt) that shows each
        student’s score per course, the average score, and the best student overall.
        """
        registered_students = {}
        filewriter= open("grades.txt", 'w')
        filewriter.write(f"Rollnum\t\t\t\tname\t\t\t\t") 
        for course in self.__courses.values():
            filewriter.write(f"\t\t{course.getCourseID()}") 
            for student in course.getClasslist():
                if student.getRollNum() in registered_students.keys():
                    continue
                registered_students[student.getRollNum()]=student
        filewriter.write(f"\t\tavg\t\t") 
        grades=[]
        for key, values in registered_students.items(): # loop through all student dictionary
            student_course_detail_marks=[key,values.getName()]
            total_marks=0
            for course in self.__courses.values():
                for stud in course.getClasslist():
                    if stud.getRollNum()!=values.getRollNum():
                        continue
                    student_course_detail_marks.append(stud.percentageGen())
                    total_marks=total_marks+stud.percentageGen()
            student_course_detail_marks.append(total_marks/5)
            grades.append(student_course_detail_marks)
        grades.sort(key = lambda x: x[7])
        for grade in grades:
            filewriter.write(f"\n{grade[0]}\t\t{grade[1]}\t\t\t\t\t\t{grade[2]}\t\t{grade[3]}\t\t{grade[4]}\t\t{grade[5]}\t\t{grade[6]}\t\t{grade[7]}\t\t\n") 
            if grade[7]== grades[-1][7]:
                filewriter.write(f"\nBest Student: {grade[1]}")
        filewriter.close()

    def gradesByCourseId(self, courseId):
        """
        A method that receives a course_id and displays each student
        and grade for all students in the course. It searches for the course_id in the
        dictionary, retrieves the respective course, and generates a file
        (courseid_grades.txt).
        """
        filewriter= open(f"{courseId}_student_grades.txt", 'w')
        course=self.__courses[courseId]
        for student in course.getClasslist():
            filewriter.write(f"{student.getRollNum()}\t\t{student.getName()}\t\t{student.percentageGen()}\t\t{student.gradeGen()}\t\t\n")
        filewriter.close()  

    def printTranscript(self,rollNumber):
        """
         A method that receives a student’s roll number and
         generates a file named in the format rollnum_transcript.txt that displays the
         student’s transcript
        """
        if self.find(rollNumber):
            filewriter= open(f"{rollNumber}_transcript.txt", 'w')
            filewriter.write(f"\n{rollNumber}\t\t")
            for course in self.__courses.values():
                for student in course.getClasslist(): 
                    if student.getRollNum()!=rollNumber:
                        continue
                    filewriter.write(f"{student.getName()}\n")
                break    
            for key, value in self.__courses.items():
                for student in value.getClasslist():
                        if rollNumber != student.getRollNum():
                            continue
                        filewriter.write(f"{key}\t\t{value.getCourseName()} \t\t{student.percentageGen()}\t\t{student.gradeGen()}\n")
        filewriter.close()

    def generateTranscripts(self):
        """
        A method that generate a file (transcripts.txt) and shows all
        student transcripts.
        """
        list_of_students=[]
        available_courses= self.getCourses()
        filewriter= open(f"transcripts.txt", 'w')
        for course in available_courses.values():
            for student in course.getClasslist():
                if [student.getRollNum(),student.getName()] in list_of_students:
                    continue
                list_of_students.append([student.getRollNum(),student.getName()])
                    
        list_of_students.sort(key = lambda x: x[0])
        for student in list_of_students:
            filewriter.write("-"*80)
            filewriter.write("\n\n\n")

            filewriter.write(f"\n{student[0]}\t\t{student[1]}\n")
            for course in available_courses.values():
                for std in course.getClasslist():
                    #print(student)
                    if std.getRollNum()!=student[0]:
                        continue
                    filewriter.write(f"{course.getCourseID()}\t\t{course.getCourseName()}\t\t\
                        {std.percentageGen()}\t\t{std.gradeGen()}\n")
            filewriter.write("\n")
            filewriter.write("-"*80)
        filewriter.close()
         

def testGradeBook():
    """
    Your code to initiate GradeBook and generate the required output files.
    """
    gradebook= GradeBook()
    gradebook.readCourses()
    print(gradebook.find('S1002'))
    
    gradebook.passedAllCourses()
    gradebook.failedStudents()
    gradebook.generateTranscripts()
    gradebook.studentsGrade()
    gradebook.printTranscript('S1000')
    gradebook.printTranscript('S1006')
    gradebook.gradesByCourseId('18751 RW')


testGradeBook()
#course1.txt,course2.txt,course3.txt,course4.txt,course5.txt