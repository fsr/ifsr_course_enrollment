from course_manager.models.Users.Executive import Executive
from course_manager.models.Users.Organizer import Organizer
from course_manager.models.Users.Tutor import Tutor
from django.contrib.auth.models import Group
from course_manager.models.CourseManagement import CourseManagement
from course_manager.models.UserManagement import UserManagement
from course_manager.models.Management import Management
from course_manager.models.Course import Course
from course_manager.models.Appointment import Appointment
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout


def show_form_login(request):
    """
    This view shows our login-site and initializes our database if necessary.\n
    When the login-site is loaded, this view checks if groups have been stored\n
    within our database and creates them if necessary to ensure full\n
    login-functionality.\n
    \n
    For testing purposes, this view may create some accounts, courses and appointments. \n

    :param request: the incoming request
    :return: rendered login-site
    """

    # logout user if he or she navigates back to this page from an executive-view
    logout(request)

    # define account for exception handling
    account = Executive
    # tutor_account_1 = Tutor
    # tutor_account_2 = Tutor
    app1 = Appointment
    app2 = Appointment

    # initialize our User Groups...
    count_of_organizers = len(Group.objects.filter(name="Organizers"))
    count_of_tutors = len(Group.objects.filter(name="Tutors"))
    if count_of_organizers is 0:
        Group.objects.create(name="Organizers")
    if count_of_tutors is 0:
        Group.objects.create(name="Tutors")

    # initialize management objects...
    if not(Management.objects.all()):
        m = Management(None)
        m.save()
    if not(CourseManagement.objects.all()):
            cm = CourseManagement(my_management=Management.objects.all()[0])
            cm.save()
    if not(UserManagement.objects.all()):
        um = UserManagement(my_management=Management.objects.all()[0])
        um.save()

    # if management has been initialized,
    # create a test Organizer and two Tutors for testing
    else:
        if not Organizer.objects.all():
            # create a unique organizer account with the custom UserManager
            # try:


            account = Organizer.objects.create_user(
                email="ifsrcourse@gmail.com",
                password="test",
                name_of_user="Horatio Cane",
                s_number="s196456"
            )

            # not catching these exceptions anymore, vvvvvvvv
            # if something goes wrong i want to know vvvvvvvv

            # catch exception when UNIQUE constraint fails
            # except IntegrityError as e:
            #     print(e.__cause__)
            # # catch exception when account could not be created
            # except (KeyError, account.DoesNotExist):
            #     print("account exception 2")
            # # if everything went well, proceed to model-object creation
            # else:
            #     print("account success")

        # for test purposes, we create a course with several appointments and assign tutors to it
        if not (Course.objects.all()):
            test_course = Course(name="Django unchained",
                                 my_course_management=CourseManagement.objects.all()[0],
                                 is_visible=True)
            test_course.save()
            app1 = Appointment(my_course=test_course,
                               weekday="Monday",
                               lesson="1.DS",
                               location="here",
                               attendance=15,
                               additional_information="nstr",
                               is_visible=True)
            app1.save()
            app2 = Appointment(my_course=test_course,
                               weekday="Monday",
                               lesson="5.DS",
                               location="over there",
                               attendance=15,
                               additional_information="nstr",
                               is_visible=True)
            app2.save()

        if not Tutor.objects.all() and Appointment.objects.all().count() > 0:
            print("Tutors!")
            # create a unique user account with the custom UserManager


            # try:
            tutor_account_1 = Tutor.objects.create_user(
                email="bud@chickenfattening.org",
                password="spencer",
                name_of_user="Bud Spencer",
                s_number="s198385"
            )

            # not catching these exceptions anymore, vvvvvvvv
            # if something goes wrong i want to know vvvvvvvv


            # # catch exception when UNIQUE constraint fails
            # except IntegrityError as e:
            #     print(e.__cause__)
            # # catch exception when account could not be created
            # except (KeyError, tutor_account_1.DoesNotExist):
            #     print("account exception 2")
            # # if everything went well, proceed to model-object creation
            # else:
            #     print("account success t1")

            # create a unique user account with the custom UserManager
            # try:
            tutor_account_2 = Tutor.objects.create_user(
                email="terrence@chickenfattening.org",
                password="hill",
                name_of_user="Terrence Hill",
                s_number="s195585"
            )
            # # catch exception when UNIQUE constraint fails
            # except IntegrityError as e:
            #     print(e.__cause__)
            # # catch exception when account could not be created
            # except (KeyError, tutor_account_2.DoesNotExist):
            #     print("account exception 2")
            # # if everything went well, proceed to model-object creation
            # else:
            #     print("account success t2")

            # lets assign tutor 1 to both appointments
            if tutor_account_1 and app1:
                app1.add_tutor(tutor_account_1)
                if app2:
                    app2.add_tutor(tutor_account_1)

    form = None
    return render(request, 'cmanagement/login.html', {'form': form})


def login_executive(request):
    """
    This view processes the POST data coming from the login-form\n
    and redirects the request respectively.\n

    :param request: the incoming request
    :return: HttpResponseRedirect()
    """
    imago = Executive
    mail_address = request.POST.get('inputEmail', '')
    password = request.POST.get('inputPassword', None)

    # find a matching Executive in our database by using the provided email-adress
    try:
        imago = Executive.objects.get(email=mail_address)
    except (KeyError, imago.DoesNotExist):
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    else:
        username = imago.username

    # if we get no POST data, redirect to the Login-Form
    if not mail_address:
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))

    user = authenticate(username=username, email=mail_address, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # check user groups for Tutor or Organizer membership (in hierarchical order)
            if user.groups.filter(name="Organizers").count() is not 0:
                # redirect to organizer view
                return HttpResponseRedirect(reverse('cmanagement:exec'))
            elif user.groups.filter(name="Tutors").count() is not 0:
                # redirect to tutor view
                return HttpResponseRedirect(reverse('cmanagement:tut'))
            else:
                # strange membership, redirect to login page
                logout(request)
                return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))

        else:
            # return to 'disabled account ' error page
            return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    else:
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))