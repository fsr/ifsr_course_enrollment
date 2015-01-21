from django.contrib.auth.decorators import login_required
from course_manager.models.Management import Management
from course_manager.models.CourseManagement import CourseManagement
from course_manager.models.UserManagement import UserManagement
from course_manager.models.Course import Course
from course_manager.models.Appointment import Appointment
from course_manager.models.Users.Tutor import Tutor
from course_manager.models.Users.Participant import Participant
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import logout
from django.utils import timezone


@login_required
def executives_index(request):
    """
    This is the main organizer page.\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :return: rendered organizer main page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    # look for expired participant accounts
    for participant in Participant.objects.all():
        # check time limit
        if not participant.is_active and participant.check_time_limit(timezone.now()):
            print(participant.name_of_user + " overtime, removing...")
            participant.delete()

    tutors_list = Tutor.objects.order_by('-date_joined')[:5]
    latest_courses_list = Course.objects.order_by('-name')[:5]

    managements = Management.objects.all()
    user_managements = UserManagement.objects.all()
    course_managements = CourseManagement.objects.all()

    context = {'tutors_list': tutors_list,
               'latest_courses_list': latest_courses_list,
               'managements': managements,
               'umanagements': user_managements,
               'cmanagements': course_managements}
    return render(request, 'cmanagement/organizer.html', context)


@login_required
def show_all_courses(request):
    """
    shows all courses\n
    \n
    For security reasons we check the user's group association\n
    and redirect if necessary.\n

    :param request: the incoming request
    :return: rendered overview page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    # look for expired participant accounts
    for participant in Participant.objects.all():
        # check time limit
        if not participant.is_active and participant.check_time_limit(timezone.now()):
            print(participant.name_of_user + " overtime, removing...")
            participant.delete()

    tutors_list = Tutor.objects.order_by('-date_joined')[:5]
    latest_courses_list = Course.objects.order_by('-name')[:5]

    all_tutors_list = Tutor.objects.order_by('-date_joined')
    all_latest_courses_list = Course.objects.order_by('-name')

    context = {'tutors_list': tutors_list,
               'latest_courses_list': latest_courses_list,
               'all_tutors_list': all_tutors_list,
               'all_latest_courses_list': all_latest_courses_list,
               'show_courses': True}
    return render(request, 'cmanagement/orga_show_overview.html', context)


@login_required
def show_all_tutors(request):
    """
    shows all tutors\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :return: rendered overview page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    # look for expired participant accounts
    for participant in Participant.objects.all():
        # check time limit
        if not participant.is_active and participant.check_time_limit(timezone.now()):
            print(participant.name_of_user + " overtime, removing...")
            participant.delete()

    tutors_list = Tutor.objects.order_by('-date_joined')[:5]
    latest_courses_list = Course.objects.order_by('-name')[:5]

    all_tutors_list = Tutor.objects.order_by('-date_joined')
    all_latest_courses_list = Course.objects.order_by('-name')

    context = {'tutors_list': tutors_list,
               'latest_courses_list': latest_courses_list,
               'all_tutors_list': all_tutors_list,
               'all_latest_courses_list': all_latest_courses_list,
               'show_courses': False}
    return render(request, 'cmanagement/orga_show_overview.html', context)


@login_required
def show_course_appointments(request, course_id):
    """
    This view displays all appointments associated to the\n
    selected course.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param course_id: database id of the selected course
    :return: rendered overview page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    try:
        course = get_object_or_404(Course, pk=course_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    if course is None:
        return HttpResponseRedirect(reverse('cmanagement:exec'))

    tutors_list = Tutor.objects.order_by('-date_joined')[:5]
    latest_courses_list = Course.objects.order_by('-name')[:5]

    course_apps = []
    appointment_list = Appointment.objects.order_by('-current_count_of_participants')
    for app in appointment_list:
        if app.my_course.id == course.id:
            course_apps.append(app)

    context = {'course': course,
               'appointment_list': course_apps,
               'tutors_list': tutors_list,
               'latest_courses_list': latest_courses_list,
               'add_not_edit': True}

    return render(request, 'cmanagement/orga_edit_appointments.html', context)


@login_required
def show_edit_appointments(request, app_id):
    """
    This view provides an interface for appointment editing.\n
    It shows the "edit appointment" form.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param app_id: database id of the selected appointment
    :return: rendered page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    try:
        app = get_object_or_404(Appointment, pk=app_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    if app is None:
        return HttpResponseRedirect(reverse('cmanagement:exec'))

    course = app.my_course
    tutors_list = Tutor.objects.order_by('-date_joined')[:5]
    latest_courses_list = Course.objects.order_by('-name')[:5]

    context = {'course': course,
               'app': app,
               'tutors_list': tutors_list,
               'latest_courses_list': latest_courses_list,
               'add_not_edit': False}

    return render(request, 'cmanagement/orga_edit_appointments.html', context)


@login_required
def show_add_appointments(request, course_id):
    """
    This view provides an interface to add appointments to an existing course.\n
    It shows the "add appointment to course" form.\n
    After a new course has been created, this view is called by default.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param course_id: database id of the selected course
    :return: rendered page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    try:
        course = get_object_or_404(Course, pk=course_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    if course is None:
        return HttpResponseRedirect(reverse('cmanagement:exec'))

    tutors_list = Tutor.objects.order_by('-date_joined')[:5]
    latest_courses_list = Course.objects.order_by('-name')[:5]

    context = {'course': course,
               'tutors_list': tutors_list,
               'latest_courses_list': latest_courses_list,
               'add_not_edit': True}

    return render(request, 'cmanagement/orga_edit_appointments.html', context)


@login_required
def edit_appointment(request, app_id):
    """
    This view processes POST data from the "edit appointment" form.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param app_id: database id of the selected appointment
    :return: HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    try:
        app = get_object_or_404(Appointment, pk=app_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    if app is None:
        return HttpResponseRedirect(reverse('cmanagement:exec'))

    weekday = request.POST.get('newweekday', '')
    lesson = request.POST.get('newlesson', '')
    location = request.POST.get('newlocation', '')
    size = request.POST.get('newsize', 0)
    info = request.POST.get('newinfo', '')
    only_organizers_see = request.POST.get('enabled', False)

    app.weekday = weekday
    app.lesson = lesson
    app.location = location
    app.attendance = size
    app.additional_information = info
    app.is_visible = not only_organizers_see
    app.save()

    return HttpResponseRedirect(reverse('cmanagement:showCourseAppointments', args=[app.my_course.id]))


@login_required
def add_appointment(request, course_id):
    """
    This view processes POST data from the "add appointment to course" form.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param course_id: database id of the selected course
    :return: HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    imago = Tutor

    try:
        course = get_object_or_404(Course, pk=course_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    weekday = request.POST.get('weekday', 'monday')
    lesson = request.POST.get('lesson', '')
    tutor = request.POST.get('tutor', '')
    location = request.POST.get('location', '')
    size = request.POST.get('size', '')
    info = request.POST.get('info', '')
    tutor = tutor.replace(" ", "")
    only_organizers_see = request.POST.get('enabled', False)

    print(weekday + ", t:" + tutor)

    try:
        imago = Tutor.objects.get(username=tutor)
    except (KeyError, imago.DoesNotExist):
        return HttpResponseRedirect(reverse('cmanagement:newAppointmentForm', args=course_id))
    else:
        if course is not None:
            app1 = Appointment(my_course=course,
                               weekday=weekday,
                               lesson=lesson,
                               location=location,
                               attendance=size,
                               additional_information=info,
                               is_visible=not only_organizers_see)
            app1.save()
            app1.add_tutor(imago)
            imago.save()

            print("added new appointment")

            return HttpResponseRedirect(reverse('cmanagement:showCourseAppointments', args=[course_id]))


@login_required
def delete_appointment(request, app_id):
    """
    This view is used to delete an appointment from the database.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param app_id: database id of the selected appointment
    :return: rendered page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    # # /todo unused 'request'
    try:
        app = get_object_or_404(Appointment, pk=app_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    if app is None:
        # error, redirect
        return HttpResponseRedirect(reverse('cmanagement:exec'))

    course_id = app.my_course.id
    app.delete()

    # success, redirect to "show appointment page"
    return HttpResponseRedirect(reverse('cmanagement:showCourseAppointments', args=[course_id]))


@login_required
def show_add_course(request):
    """
    This view provides an interface to create new courses.\n
    It shows the "add course" form.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :return: rendered page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    tutors_list = Tutor.objects.order_by('-date_joined')[:5]
    latest_courses_list = Course.objects.order_by('-name')[:5]

    context = {'tutors_list': tutors_list,
               'latest_courses_list': latest_courses_list, }

    return render(request, 'cmanagement/orga_add_course.html', context)


@login_required
def add_course(request):
    """
    This view processes POST data from the "add course" form.\n
    On success, it creates a new course object.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :return: HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    name = request.POST.get('name', '')
    only_organizers_see = request.POST.get('enabled', False)
    new_course = None
    try:
        new_course = Course(name=name,
                            my_course_management=CourseManagement.objects.all()[0],
                            is_visible=not only_organizers_see)
    # # /todo 'DoesNotExist' not resolved
    except (KeyError, new_course.DoesNotExist):
        print("new course exception 1")
        # error, redirect to main organizer page
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        new_course.save()
        # success, redirect to "add new appointment page"
        return HttpResponseRedirect(reverse('cmanagement:newAppointmentForm', args=[new_course.id]))


@login_required
def delete_course(request, course_id):
    """
    This view deletes a selected course from the database.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param course_id: database id of the selected appointment
    :return: HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    # # \todo unused 'request'
    try:
        course = get_object_or_404(Course, pk=course_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    if course is None:
        #error, redirect to "add new appointment page"
        return HttpResponseRedirect(reverse('cmanagement:newAppointmentForm', args=[course.id]))

    course.delete()

    #success, redirect to "add new appointment page"
    return HttpResponseRedirect(reverse('cmanagement:exec'))


@login_required
def toggle_course_visibility(request, course_id):
    """
    This view toggles the selected courses visibility.\n
    When the selected courses "is_visible" attribute is set to "False"\n
    the selected course is visible to organizers only.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param course_id: database id of the selected course
    :return: HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    # # \todo unused 'request'
    try:
        course = get_object_or_404(Course, pk=course_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    if course is None:
        #error, redirect to "add new appointment page"
        return HttpResponseRedirect(reverse('cmanagement:showCourseAppointments', args=[course.id]))

    course.is_visible = not course.is_visible
    course.save()

    #success, redirect to "add new appointment page"
    return HttpResponseRedirect(reverse('cmanagement:showCourseAppointments', args=[course.id]))


@login_required
def show_assign_tutor_to_app(request, app_id):
    """
    This view provides an interface for appointment editing.\n
    It shows the "assign/remove tutor" form.\n
    Tutors can be selected from a list and can then be assigned\n
    or removed to/from the selected appointment.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param app_id: database id of the selected appointment
    :return: rendered page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    try:
        app = get_object_or_404(Appointment, pk=app_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    # redirect to error page if appointment could not be loaded
    if app is None:
        return HttpResponseRedirect(reverse('cmanagement:exec'))

    course = app.my_course
    tutors_list = Tutor.objects.order_by('-date_joined')[:5]
    latest_courses_list = Course.objects.order_by('-name')[:5]

    context = {'app': app,
               'tutors_list': tutors_list,
               'latest_courses_list': latest_courses_list,
               'course': course}

    return render(request, 'cmanagement/orga_assign_tutor.html', context)


@login_required
def assign_tutor_to_app(request, app_id):
    """
    This view processes POST data from the "assign/remove tutor" form.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param app_id: database id of the selected appointment
    :return: HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    try:
        app = get_object_or_404(Appointment, pk=app_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    # redirect to error page if appointment could not be loaded
    if app is None:
        return HttpResponseRedirect(reverse('cmanagement:exec'))

    name = request.POST.get('tutors_radio', '')
    mode = request.POST.get('radio', 'assign')
    name = name.replace(" ", "")

    imago = Tutor
    try:
        imago = Tutor.objects.get(username=name)
    except (KeyError, imago.DoesNotExist):
        return HttpResponseRedirect(reverse('cmanagement:assignTutorForm', args=[app_id]))
    else:
        if mode == 'assign':
            app.add_tutor(imago)
        else:
            app.remove_tutor(imago)

        imago.save()
        print(mode, name)
        # success, redirect to overview page
        return HttpResponseRedirect(reverse('cmanagement:showCourseAppointments', args=[app.my_course.id]))


@login_required
def show_edit_tutor(request, tutor_id):
    """
    This view provides an interface for tutor editing.\n
    It shows the "edit tutor" form.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param tutor_id: database id of the selected tutor
    :return: rendered page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    try:
        tutor = get_object_or_404(Tutor, pk=tutor_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    # redirect to error page if tutor could not be loaded
    if tutor is None:
        return HttpResponseRedirect(reverse('cmanagement:exec'))

    tutors_list = Tutor.objects.order_by('-date_joined')[:5]
    latest_courses_list = Course.objects.order_by('-name')[:5]
    edit_not_create = True

    context = {'edit_not_create': edit_not_create,
               'tutor': tutor,
               'tutors_list': tutors_list,
               'latest_courses_list': latest_courses_list, }

    return render(request, 'cmanagement/orga_edit_tutor.html', context)


@login_required
def delete_tutor(request, tutor_id):
    """
    This view removes the selected tutor from the database.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param tutor_id: database id of the selected tutor
    :return: HttpResponseRedirect()
    """
    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    try:
        tutor = get_object_or_404(Tutor, pk=tutor_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    if tutor is None:
        # error, redirect to "add new appointment page"
        return HttpResponseRedirect(reverse('cmanagement:editTutorForm', args=[tutor.id]))

    tutor.delete()

    # success, redirect to "add new appointment page"
    return HttpResponseRedirect(reverse('cmanagement:exec'))


@login_required
def edit_tutor(request, tutor_id):
    """
    This view processes POST data from the "edit tutor" form.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param tutor_id: database id of the selected tutor
    :return: rendered page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    try:
        tutor = get_object_or_404(Tutor, pk=tutor_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    # redirect to error page if tutor could not be loaded
    if tutor is None:
        return HttpResponseRedirect(reverse('cmanagement:exec'))

    name = request.POST.get('name', '')
    email = request.POST.get('email', '')
    only_organizers_see = request.POST.get('enabled', False)
    username = name
    username = username.replace(" ", "")

    print("new username: " + username)
    print("new email: " + email)

    if only_organizers_see:
        print("tutor hidden")
    else:
        print("tutor activated")

    Tutor.objects.edit_tutor(tutor, name, tutor.s_number, email, not only_organizers_see)

    # success, redirect to main organizer page
    return HttpResponseRedirect(reverse('cmanagement:exec'))


@login_required
def show_create_tutor_form(request):
    """
    This view provides an interface to create new tutors.\n
    It shows the "add tutor" form.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :return: rendered page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    tutors_list = Tutor.objects.order_by('-date_joined')[:5]
    latest_courses_list = Course.objects.order_by('-name')[:5]
    edit_not_create = False

    context = {'edit_not_create': edit_not_create,
               'tutors_list': tutors_list,
               'latest_courses_list': latest_courses_list, }

    return render(request, 'cmanagement/orga_edit_tutor.html', context)


@login_required
def create_tutor(request):
    """
    This view processes POST data from the "add tutor" form.\n
    On success, it creates a new tutor object and saves it to the database.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :return: HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    name = request.POST.get('newname', '')
    email = request.POST.get('newemail', '')
    s_number = request.POST.get('s_number', 's0000000')

    first_password = Tutor.objects.make_random_password()
    new_tutor_account = Tutor

    # create a unique user account with the custom UserManager
    try:
        new_tutor_account = Tutor.objects.create_user(email=email,
                                                      password=first_password,
                                                      name_of_user=name,
                                                      s_number=s_number)
    # catch exception when UNIQUE constraint fails
    except IntegrityError as e:
        print(e.__cause__)
        # error, redirect to main organizer page
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    # catch exception when account could not be created
    except (KeyError, new_tutor_account.DoesNotExist):
        print("account exception 2")
        # error, redirect to main organizer page
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    # if everything went well, proceed to model-object creation
    else:
        print("account success t1")
        # send the first password to the new tutor
        message = "Hello new Tutor! \nThis is your first password: " + first_password + \
                  " \nPlease sign in and change your password."
        recipient = new_tutor_account
        subject = "Your Tutor registration. From " + request.user.username + " to " + recipient.username
        from_email = request.user.email
        recipient = recipient.email

        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, [recipient])
            except BadHeaderError:
                # error, redirect to main organizer page
                return HttpResponseRedirect(reverse('cmanagement:exec'))
            else:
                # success, redirect to main organizer page
                return HttpResponseRedirect(reverse('cmanagement:noteTutSuccOrga'))
        else:
            # error, redirect to main organizer page
            return HttpResponseRedirect(reverse('cmanagement:exec'))


@login_required
def show_course_credits(request, course_id):
    """
    This view displays an overview of credit data.\n
    It shows a list of all course participants who posted\n
    credit and faculty information on course enrollment.\n
    \n
    NOTICE: The same participant may appear multiple times on\n
            the list if he/she stated different credit information.\n
    \n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param course_id: database id of the selected course
    :return: rendered page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    try:
        course = get_object_or_404(Course, pk=course_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    if course is None:
        return HttpResponseRedirect(reverse('cmanagement:exec'))

    tutors_list = Tutor.objects.order_by('-date_joined')[:5]
    latest_courses_list = Course.objects.order_by('-name')[:5]

    part_list = []
    course_apps = []
    appointment_list = Appointment.objects.order_by('-current_count_of_participants')
    for appl in appointment_list:
        if appl.my_course.id == course.id:
            course_apps.append(appl)
            for participant in appl.my_participants.all():
                if not participant.credit == 'none':
                    part_list.append(participant)

    context = {'course': course,
               'part_list': part_list,
               'tutors_list': tutors_list,
               'latest_courses_list': latest_courses_list,
               'logged_in_user': request.user}

    return render(request, 'cmanagement/orga_show_credit_data.html', context)


@login_required
def show_appointment_participants(request, app_id):
    """
    This view displays a list of all participants associated with\n
    the selected appointment.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param app_id: database id of the selected appointment
    :return: rendered page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    try:
        app = get_object_or_404(Appointment, pk=app_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    if app is None:
        return HttpResponseRedirect(reverse('cmanagement:exec'))

    course = app.my_course

    tutors_list = Tutor.objects.order_by('-date_joined')[:5]
    latest_courses_list = Course.objects.order_by('-name')[:5]

    course_apps = []
    appointment_list = Appointment.objects.order_by('-current_count_of_participants')
    for appl in appointment_list:
        if appl.my_course.id == course.id:
            course_apps.append(appl)

    part_list = app.my_participants.all()

    show_not_add = True

    context = {'course': course,
               'app': app,
               'part_list': part_list,
               'tutors_list': tutors_list,
               'course_list': latest_courses_list,
               'logged_in_user': request.user,
               'show_not_add': show_not_add}

    return render(request, 'cmanagement/orga_edit_participants.html', context)


@login_required
def show_add_participant(request, app_id):
    """
    This view provides an interface to create new participants.\n
    It shows the "add participant" form.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param app_id: database id of the selected appointment
    :return: rendered page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    try:
        app = get_object_or_404(Appointment, pk=app_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    if app is None:
        return HttpResponseRedirect(reverse('cmanagement:exec'))

    course = app.my_course

    tutors_list = Tutor.objects.order_by('-date_joined')[:5]
    latest_courses_list = Course.objects.order_by('-name')[:5]

    course_apps = []
    appointment_list = Appointment.objects.order_by('-current_count_of_participants')
    for appl in appointment_list:
        if appl.my_course.id == course.id:
            course_apps.append(appl)

    part_list = app.my_participants.all()
    show_not_add = False

    context = {'course': course,
               'app': app,
               'part_list': part_list,
               'tutors_list': tutors_list,
               'course_list': latest_courses_list,
               'logged_in_user': request.user,
               'show_not_add': show_not_add}

    return render(request, 'cmanagement/orga_edit_participants.html', context)


@login_required
def add_participant_done(request, app_id):
    """
    This view processes POST data from the "add participant" form.\n
    On success, it creates a new participant object, associates it with\n
    the selected appointment and saves it to the database.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param app_id: database id of the selected appointment
    :return: HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    try:
        selected_appointment = get_object_or_404(Appointment, pk=app_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    s_number = request.POST.get('snumber', '')
    e_mail = request.POST.get('inputEmail', '')
    add_mode = request.POST.get('radio', 'r0')

    if not selected_appointment:
        return HttpResponseRedirect(reverse('cmanagement:showAppointmentPart', args=[app_id]))

    # if "add by s-number" is selected we need a s-number
    # # \todo: show some kind of notification or error message
    if add_mode == 'r0' and not s_number:
        return HttpResponseRedirect(reverse('cmanagement:showAddPart', args=[app_id]))

    # if "add by email" is selected we need an email adress
    ## \todo: show some kind of notification or error message
    if add_mode == 'r1' and not e_mail:
        return HttpResponseRedirect(reverse('cmanagement:showAddPart', args=[app_id]))

    s_number = s_number.replace(" ", "")
    if add_mode == 'r0':
        email = s_number + "@mail.zih.tu-dresden.de"
        username = s_number
    else:
        email = e_mail
        username = e_mail
        s_number = '- no s-number -'

    # first, check the database for a matching participant
    new_account = None #Participant

    for account in Participant.objects.all():
        if account.username == username:
            new_account = account
            break

    if not new_account:
        # create a unique user account with the custom UserManager
        try:
            new_account = Participant.objects.create_user(username=username,
                                                          email=email,
                                                          name_of_user=username,
                                                          s_number=s_number, )

        # catch exception when UNIQUE constraint fails
        except IntegrityError as e:
            print(e.__cause__)
            # error, redirect
            return HttpResponseRedirect(reverse('cmanagement:showAppointmentPart', args=[app_id]))
        # catch exception when account could not be created
        except (KeyError, new_account.DoesNotExist):
            print("account exception 2")
            # error, redirect
            return HttpResponseRedirect(reverse('cmanagement:showAppointmentPart', args=[app_id]))
        # if everything went well, proceed
        else:
            pass

    # assign our participant to the selected appointment
    print("account success t1")
    selected_appointment.add_participant(new_account)
    new_account.save()

    # send confirmation email to participant
    message = "Hello! \nYou have been signed in to:" + selected_appointment.my_course.name + "/" \
              + selected_appointment.weekday + "/" + selected_appointment.lesson + "/" + selected_appointment.location
    recipient = new_account
    subject = "IFSR course registration (" + selected_appointment.my_course.name + ")"
    from_email = "ifsrcourses@gmail.com"
    recipient = recipient.email

    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, [recipient])
        except BadHeaderError:
            # error, redirect to main organizer page
            return HttpResponseRedirect(reverse('cmanagement:exec'))
        else:
            # success, redirect to overview page
            return HttpResponseRedirect(reverse('cmanagement:showAppointmentPart', args=[app_id]))
    else:
        # error, redirect to main organizer page
        return HttpResponseRedirect(reverse('cmanagement:exec'))


@login_required
def delete_participant(request, part_id, app_id):
    """
    This view removes the selected participant from the database.\n
    The associated appointment is needed to navigate back to the\n
    appointments "show participants" page after the selected participant\n
    has been deleted.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param app_id: database id of the associated appointment
    :param part_id: database id of the selected participant
    :return: HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    try:
        part = get_object_or_404(Participant, pk=part_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    try:
        app = get_object_or_404(Appointment, pk=app_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    if part is None or app is None:
        # error, redirect
        return HttpResponseRedirect(reverse('cmanagement:exec'))

    # first, remove from app, then maybe part.delete() if no assignments left for part
    app.remove_participant(part)

    if not part:
        print("part removed!!!!????")
    else:
        print("part still there!!!!")

    part.save()
    # check for other assignments
    b_enrolled = False
    for appointment in Appointment.objects.all():
        for participant in appointment.my_participants.all():
            if participant.username == part.username:
                b_enrolled = True

    if not b_enrolled:
        print(" no other appointments for "+part.username+" found, deleting...")
        part.delete()

    #print(Participant.objects.all())

    # success, redirect
    return HttpResponseRedirect(reverse('cmanagement:showAppointmentPart', args=[app_id]))


@login_required
def show_notification_email_success(request):
    """
    displays a notification specified in 'message'\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :return: rendered page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    message = "E-Mail has been sent successfully!"

    context = {'message': message}

    return render(request, 'cmanagement/orga_notification.html', context)


@login_required
def show_notification_addtutor_success(request):
    """
    displays a notification specified in 'message'\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :return: rendered page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    message = "Tutor added successfully!"

    context = {'message': message}

    return render(request, 'cmanagement/orga_notification.html', context)