from django.contrib.auth.decorators import login_required
from course_manager.models.Users.Participant import Participant
from course_manager.models.Course import Course
from course_manager.models.Appointment import Appointment
from course_manager.models.Users.Tutor import Tutor
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from course_manager.util.courses import make_courses_list, make_other_tutors_list, compile_course_apps


@login_required
def tutor_index(request):
    """
    This is the main tutor page.\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :return: rendered tutor main page or HttpResponseRedirect()
    """
    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:index'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # redirect to organizer view
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # everything is fine, proceed to tutor's view
        pass
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:index'))
     # <SECURITY_BLOCK>
    other_tutors_list = []
    tutors_list = Tutor.objects.all()

    for tut in tutors_list:
        if not tut.username == request.user.username and tut.is_visible:
            other_tutors_list.append(tut)

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
    context = {'tutors_list': other_tutors_list,
               'my_courses_list': my_courses_list,
               'logged_in_user': request.user}
    return render(request, 'cmanagement/tutor_welcome.html', context)


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
        return HttpResponseRedirect(reverse('cmanagement:index'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # redirect to organizer view
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # everything is fine, proceed to tutor's view
        pass
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:index'))
     # <SECURITY_BLOCK>

    try:
        course = get_object_or_404(Course, pk=course_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        pass

    if course is None:
        return HttpResponseRedirect(reverse('cmanagement:tut'))

    other_tutors_list = []
    tutors_list = Tutor.objects.all()

    for tut in tutors_list:
        if not tut.username == request.user.username and tut.is_visible:
            other_tutors_list.append(tut)

    my_courses_list = []
    course_apps = []
    for appl in Appointment.objects.all():
        if appl.is_visible:
            for tut in appl.my_tutors.all():
                if tut.username == request.user.username and appl.my_course.is_visible:
                    course_apps.append(appl)
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

    context = {'course': course,
               'appointment_list': course_apps,
               'tutors_list': other_tutors_list,
               'my_courses_list': my_courses_list,
               'logged_in_user': request.user}

    return render(request, 'cmanagement/tutor_appointments.html', context)


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
        return HttpResponseRedirect(reverse('cmanagement:index'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # redirect to organizer view
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # everything is fine, proceed to tutor's view
        pass
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:index'))
     # <SECURITY_BLOCK>

    try:
        app = get_object_or_404(Appointment, pk=app_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        pass

    if app is None:
        return HttpResponseRedirect(reverse('cmanagement:tut'))

    course = app.my_course
    other_tutors_list = make_other_tutors_list(request)


    my_courses_list = make_courses_list(request)

    # This variable is unused???
    course_apps = compile_course_apps(course)

    part_list = app.my_participants.all()

    context = {'course': course,
               'app': app,
               'part_list': part_list,
               'tutors_list': other_tutors_list,
               'my_courses_list': my_courses_list,
               'logged_in_user': request.user}

    return render(request, 'cmanagement/tutor_show_participants.html', context)


@login_required
def delete_participant(request, part_id):
    """
    This view removes the selected participant from the database.\n
    The associated appointment is needed to navigate back to the\n
    appointments "show participants" page after the selected participant\n
    has been deleted.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param part_id: database id of the selected participant
    :return: HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:index'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # redirect to organizer view
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # everything is fine, proceed to tutor's view
        pass
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:index'))
     # <SECURITY_BLOCK>

    try:
        part = get_object_or_404(Participant, pk=part_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        pass

    if part is None:
        #error, redirect
        return HttpResponseRedirect(reverse('cmanagement:tut'))

    part.delete()

    #success, redirect
    return HttpResponseRedirect(reverse('cmanagement:tut'))


@login_required
def edit_appointment_location(request, app_id):
    """
    This view provides an interface for tutors to change\n
    the selected appointments location.\n
    It shows the "change appointment location" form.\n

    :param request: the incoming request
    :param app_id: database id of the selected appointment
    :return: HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:index'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # redirect to organizer view
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # everything is fine, proceed to tutor's view
        pass
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:index'))
     # <SECURITY_BLOCK>

    try:
        app = get_object_or_404(Appointment, pk=app_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        pass

    if app is None:
        return HttpResponseRedirect(reverse('cmanagement:tut'))

    course = app.my_course
    other_tutors_list = make_other_tutors_list(request)

    my_courses_list = make_courses_list(request)

    # this is unused???
    course_apps = compile_course_apps(course)

    part_list = app.my_participants.all()

    context = {'course': course,
               'app': app,
               'part_list': part_list,
               'tutors_list': other_tutors_list,
               'my_courses_list': my_courses_list,
               'logged_in_user': request.user}

    return render(request, 'cmanagement/tutor_appointment_changeloc.html', context)


@login_required
def edit_appointment_location_done(request, app_id):
    """
    This view processes POST data from the "change appointment location" form.\n

    :param request: the incoming request
    :param app_id: database id of the selected appointment
    :return: rendered page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:index'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # redirect to organizer view
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # everything is fine, proceed to tutor's view
        pass
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:index'))
     # <SECURITY_BLOCK>

    try:
        app = get_object_or_404(Appointment, pk=app_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        pass

    if app is None:
        return HttpResponseRedirect(reverse('cmanagement:tut'))

    course = app.my_course

    if course is None:
        return HttpResponseRedirect(reverse('cmanagement:tut'))

    newloc = request.POST.get('loc', '')
    app.location = newloc
    app.save()

    return HttpResponseRedirect(reverse('cmanagement:showCourseAppointmentsTut', args=[course.id]))


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
        return HttpResponseRedirect(reverse('cmanagement:index'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # redirect to organizer view
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # everything is fine, proceed to tutor's view
        pass
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:index'))
     # <SECURITY_BLOCK>

    message = "E-Mail has been sent successfully!"

    context = {'message': message}

    return render(request, 'cmanagement/orga_notification.html', context)