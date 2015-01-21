from django.contrib.auth.decorators import login_required
from course_manager.models.Appointment import Appointment
from course_manager.models.Users.Tutor import Tutor
from course_manager.models.Users.User import UserAccount
from course_manager.models.Course import Course
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, BadHeaderError, send_mass_mail
from smtplib import SMTPException
from django.contrib.auth import logout


@login_required
def show_form_email_to_course(request, course_id):
    """
    This view shows an E-Mail form.\n
    The written message will be send to all participants enrolled to\n
    appointments which are associated with the selected course\n
    and the active request user (a tutor).\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param course_id: the database id of the selected course
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
        the_course = get_object_or_404(Course, pk=course_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        pass

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
                    my_courses_list.append(appl.my_course)

    context = {'tutors_list': other_tutors_list,
               'my_courses_list': my_courses_list,
               'logged_in_user': request.user,
               'recipient': the_course,
               'mass_email': True}

    return render(request, 'cmanagement/tutor_message.html', context)


@login_required
def show_form_email(request, recipient_id):
    """
    This view shows an E-Mail form for a single recipient.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param recipient_id: the database id of the recipient user
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
        recipient = get_object_or_404(UserAccount, pk=recipient_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        pass

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
                    my_courses_list.append(appl.my_course)

    context = {'tutors_list': other_tutors_list,
               'my_courses_list': my_courses_list,
               'logged_in_user': request.user,
               'recipient': recipient,
               'mass_email': False}
    return render(request, 'cmanagement/tutor_message.html', context)


@login_required
def send_email(request, recipient_id):
    """
    This view processes POST data provided by an E-Mail form.\n
    The message will be send to a single recipient.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param recipient_id: the database id of the recipient user
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
        recipient = get_object_or_404(UserAccount, pk=recipient_id)
    except Http404:
        return HttpResponseRedirect('cmanagement:newEmailFormTut', args=[recipient_id])
    else:
        pass

    message = request.POST.get('InputMessage', '')
    subject = "Mail from "+request.user.username+" to "+recipient.username
    from_email = request.user.email
    recipient = recipient.email

    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, [recipient])
        except BadHeaderError:
            return HttpResponseRedirect('cmanagement:newEmailFormTut', args=[recipient_id])
        else:
            return HttpResponseRedirect(reverse('cmanagement:noteMailSuccTut'))
    else:
        return HttpResponseRedirect('cmanagement:newEmailFormTut', args=[recipient_id])


@login_required
def send_email_to_course(request, course_id):
    """
    This view processes POST data provided by an E-Mail form.\n
    The message will be send to all participants enrolled to\n
    appointments which are associated with the selected course\n
    and the active request user (a tutor).\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param course_id: the database id of the selected course
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
        the_course = get_object_or_404(Course, pk=course_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:newMEmailFormTut', args=[course_id]))
    else:
        pass

    course_apps = []
    for appl in Appointment.objects.all():
        if appl.is_visible:
            for tut in appl.my_tutors.all():
                if tut.username == request.user.username and appl.my_course.is_visible:
                    course_apps.append(appl)

    message = request.POST.get('message', '')
    subject = "Mail from "+request.user.username+" to course: "+the_course.name
    from_email = "ifsrcourses@gmail.com"

    recipient_list = []
    for app in course_apps:
        if app.my_course == the_course:
            for part in app.my_participants.all():
                recipient_list.append(part.email)

    # if there is no one to receive, return
    if not recipient_list:
        return HttpResponseRedirect(reverse('cmanagement:newMEmailFormTut', args=[course_id]))

    print(subject, message)
    print(recipient_list)

    if subject and message and from_email:
        try:
            data_tuple = (subject, message, from_email, recipient_list)
            send_mass_mail((data_tuple,))
        except BadHeaderError:
            return HttpResponseRedirect(reverse('cmanagement:newMEmailFormTut', args=[course_id]))
        except SMTPException:
            return HttpResponseRedirect(reverse('cmanagement:newMEmailFormTut', args=[course_id]))
        else:
            return HttpResponseRedirect(reverse('cmanagement:noteMailSuccTut'))
    else:
        return HttpResponseRedirect(reverse('cmanagement:newMEmailFormTut', args=[course_id]))