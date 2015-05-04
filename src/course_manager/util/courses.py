from course_manager.models import Tutor, Appointment

__author__ = 'Justus Adam'
__version__ = '0.1'


def make_other_tutors_list(request):
    tutors_list = Tutor.objects.all()
    return [
        tut for tut in tutors_list
        if not tut.username == request.user.username and tut.is_visible
    ]


def make_courses_list(request):
    my_courses_list = []

    for appl in Appointment.objects.all():
        if appl.is_visible:
            for tut in appl.my_tutors.all():
                if tut.username == request.user.username and appl.my_course.is_visible:
                    # check if we already have this course in our list
                    if not my_courses_list:
                        my_courses_list.append(appl.my_course)
                    else:
                        b_known = False
                        for known_course in my_courses_list:
                            if known_course.name == appl.my_course.name:
                                b_known = True
                        if not b_known:
                            my_courses_list.append(appl.my_course)

    return my_courses_list


def compile_course_apps(course):
    appointment_list = Appointment.objects.order_by('-current_count_of_participants')
    return [
        appl for appl in appointment_list
        if appl.my_course.id == course.id and appl.is_visible
    ]