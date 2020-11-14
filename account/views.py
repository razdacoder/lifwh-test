from django.shortcuts import render, redirect, get_object_or_404
from validate_email import validate_email
from django.contrib import messages
from django.contrib.messages import constants as message_contants
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import User, Subscriber, Course, Video, Contact
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
import reportlab
import stripe
stripe.api_key = 'sk_test_51Gbg4rDuJEdsRuN4M9meTFOvKfcVGH6EtqNqgjuI6kgk5oHAC8JvARZhOP0rHC5mtwqzxbwc4v0w6yaJHv3ADh4000lovgeGj7'


# Create your views here.
MESSAGE_LEVEL = message_contants.DEBUG


def index_view(request):
    return render(request, "index.html")


def register_view(request):
    if request.user.is_authenticated == True:
        return redirect("index")
    else:
        if request.method == "GET":
            return render(request, "register.html")
        else:
            first_name = request.POST.get("firstname")
            last_name = request.POST.get("lastname")
            number = request.POST.get("number")
            email = request.POST.get("email")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            is_valid = validate_email(email, verify=True)

            if password1 != password2:
                messages.error(request, "Passwords do not match")
                return redirect("register")
            elif is_valid == False:
                messages.error(request, "Invalid Email Address")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email Already Exists")
            else:
                user = User.objects.create_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    number=number
                )
                user.set_password(password1)
                user.save()
            return redirect("login")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        if request.method == "GET":
            return render(request, "login.html")
        else:
            email = request.POST.get("email")
            password = request.POST.get("password")
            remember = request.POST.get("remember")

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
            else:
                messages.error(request, "Invalid email or password")
                return redirect("login")
            return redirect("profile")


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def profile_view(request):
    return render(request, "profile.html")


@login_required(login_url="login")
def profile_pass_view(request):
    return render(request, "profile_pass.html")


@login_required(login_url="login")
def profile_not_view(request):
    return render(request, "profile_not.html")


@login_required(login_url="login")
def profile_bills_view(request):
    return render(request, "profile_bills.html")


@login_required(login_url="login")
def edit_profile_view(request):
    email = request.POST.get("email")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    number = request.POST.get("number")

    user = User.objects.get(email=request.user.email)
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.number = number
    user.save()
    messages.success(request, "Updated Successfully", extra_tags="success")
    return redirect("profile")


@login_required(login_url="login")
def edit_pass_view(request):
    password = request.POST.get("password")
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")
    # number = request.POST.get("number")

    user = User.objects.get(email=request.user.email)
    is_valid = user.check_password(password)
    if password1 != password2:
        messages.error(request, "Password do not match")
        return redirect("profile_pass")

    elif is_valid == False:
        messages.error(request, "Incorrect Password")
        return redirect("profile_pass")
    else:
        user.set_password(password1)
        user.save()
        messages.success(request, "Password Updated Succesfully")

    return redirect("profile_pass")


@login_required(login_url="login")
def subcsribe(request):
    email = request.POST.get("email")
    sub = Subscriber.objects.create(email=email)
    sub.save()

    return redirect("profile")


def courses_view(request):
    courses = Course.objects.all()
    context = {
        "courses": courses
    }

    return render(request, "courses.html", context)


# def new_course(request):
#     if request.method == 'GET':
#         return render(request, 'new-course.html')
#     else:
#         title = request.POST.get("title")
#         description = request.POST.get("description")
#         image = request.FILES.get("image")
#         pdf = request.FILES.get("pdf")
#         videos = request.FILES.getlist("videos")

#         course = Course(title=title, description=description,
#                         image=image, pdf=pdf, videos=videos)
#         course.save()
#         return redirect("course_view")




def courses_overview(request, id):
    course = get_object_or_404(Course, id=id)
    videos = Video.objects.filter(course=course)
    # print(course.videos[0].name)
    context = {
        "course": course,
        "videos": videos
    }

    return render(request, 'course_over.html', context)


@login_required(login_url="login")
def courses_start(request, id):
    course = get_object_or_404(Course, id=id)
    videos = Video.objects.filter(course=course)
    # print(course.videos[0].name)
    context = {
        "course": course,
        "videos": videos
    }

    user = get_object_or_404(User, email=request.user.email)

    if user.plan == course.plan or user.plan == "intermediate" or user.plan == "enterprise":

        idsy = []
        idsc = []
        # print(len(user.my_course))
        for ids in user.my_course:
            idsy.append(ids["course_id"])

        try:
            this_course = idsy.index(id)

            print("Yes")
        except:
            if len(user.my_course) == 0:
                user.my_course = [{"course_id": id, "progress": 0}]
            elif len(user.my_course) > 0:
                user.my_course.append({"course_id": id, "progress": 0})
            user.save()

        for ids in course.students:
            idsc.append(ids["students_id"])

        try:
            this_user = idsc.index(str(request.user.id))
        except:
            if len(course.students) == 0:
                course.students = [{"students_id": str(request.user.id)}]
            elif len(course.students) > 0:
                course.students.append({"students_id": str(request.user.id)})
            course.save()

        # if user.my_course == 0:

        print(idsy)
    else:
        messages.info(request, "Upgrade Your Plan to start this course!!!")
        print('Error')
        return redirect("/#plans")

    return render(request, 'course_start.html', context)


@login_required(login_url="login")
def profile_dashboard(request):
    user = get_object_or_404(User, email=request.user.email)

    courses = []
    print(len(user.my_course))
    for ids in user.my_course:
        # idsy.append(ids["course_id"])
        course = Course.objects.get(id=ids["course_id"])
        progress = ids["progress"]
        courses.append({"course": course, "progress": progress})

    context = {
        "courses": courses
    }

    return render(request, "dashboard.html", context)


@login_required(login_url='login')
def update_progress(request, id):
    user = get_object_or_404(User, email=request.user.email)

    courseToUpdate = get_object_or_404(Course, id=id)

    courseList = []
    # print(user.my_course[0])
    for i in user.my_course:
        courseList.append(i["course_id"])

    courseIndex = courseList.index(id)

    videos = Video.objects.filter(course=courseToUpdate)

    progressMul = int(100 / videos.count())

    progress = user.my_course[courseIndex]["progress"] + progressMul
    if progress > 100:
        progress = 100
    user.my_course[courseIndex]["progress"] = progress
    user.save()


def contact(request):
    name = request.POST.get('name')
    email = request.POST.get("email")
    message = request.POST.get("message")
    newsletter = request.POST.get("newsletter")

    contact = Contact(
        name=name,
        email=email,
        message=message
    )

    if newsletter == "on":
        sub = Subscriber(
            email=email
        )

        sub.save()
    contact.save()
    return redirect("index")


@login_required(login_url="login")
def changeplan_foundation(request):
    # Payment

    # ON payment Success
    

    user = get_object_or_404(User, email=request.user.email)
    user.plan = "foundation"
    user.save()
    return redirect("index")


@login_required(login_url="login")
def changeplan_intermediate(request):
    # Payment

    # ON payment Success

    user = get_object_or_404(User, email=request.user.email)
    user.plan = "intermediate"
    user.save()
    return redirect("index")



@login_required(login_url="login")
def changeplan_enterprise(request):
    # Payment

    # ON payment Success

    user = get_object_or_404(User, email=request.user.email)
    user.plan = "enterprise"
    user.save()
    return redirect("index")


@login_required(login_url="login")
def show_pdf(request, path):
    # # Create a file-like buffer to receive PDF data.
    # buffer = io.BytesIO()

    # # Create the PDF object, using the buffer as its "file."
    # p = canvas.Canvas(buffer)

    # # Draw things on the PDF. Here's where the PDF generation happens.
    # # See the ReportLab documentation for the full list of functionality.
    # p.drawString(100, 100, filename)

    # # Close the PDF object cleanly, and we're done.
    # p.showPage()
    # p.save()

    # # FileResponse sets the Content-Disposition header so that browsers
    # # present the option to save the file.
    # buffer.seek(0)
    # return FileResponse(buffer, as_attachment=True, filename=filename)

    # filename = employee + ".pdf"
    # filepath = os.path.join(settings.MEDIA_ROOT, "payslips", year, month, filename)
    # print(filepath)
    return FileResponse(open(path, 'rb'), content_type='application/pdf')


# Admin Panel View
def admin_login(request):
    if request.method == 'GET':
        return render(request, 'admin-login.html')
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_admin == True:
                login(request, user)
                return redirect("admin_board")
            else:
                messages.error(request, "Unauthorized User")
                return redirect("admin_login")
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('admin_login')


@login_required(login_url="admin_login")
def admin_board(request):
    courses = Course.objects.all()
    context = {
        "courses": courses
    }
    return render(request, "admin-dashboard.html", context)


@login_required(login_url="admin_login")
def admin_course(request):
    courses = Course.objects.all()
    context = {
        "courses": courses
    }
    return render(request, "admin-course.html", context)


@login_required(login_url="admin_login")
def admin_message(request):
    contacts = Contact.objects.all()
    context = {
        "contacts": contacts
    }
    return render(request, "admin-message.html", context)


@login_required(login_url="admin_login")
def admin_settings(request):
    return render(request, "admin-setting.html")


@login_required(login_url="admin_login")
def admin_edit_pass_view(request):
    password = request.POST.get("password")
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")
    # number = request.POST.get("number")

    user = User.objects.get(email=request.user.email)
    is_valid = user.check_password(password)
    if password1 != password2:
        messages.error(request, "Password do not match")
        return redirect("admin-settings")

    elif is_valid == False:
        messages.error(request, "Incorrect Password")
        return redirect("admin-settings")
    else:
        user.set_password(password1)
        user.save()
        messages.success(request, "Password Updated Succesfully")

    return redirect("admin-settings")


@login_required(login_url="admin_login")
def admin_edit_profile_view(request):
    email = request.POST.get("email")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    number = request.POST.get("number")

    user = User.objects.get(email=request.user.email)
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.number = number
    user.save()
    messages.success(request, "Updated Successfully", extra_tags="success")
    return redirect("admin-settings")


@login_required(login_url="admin_login")
def admin_course_add(request):
    if request.method == "GET":
        return render(request, "newCourse.html")
    else:
        title = request.POST.get("title")
        des = request.POST.get("des")
        plan = request.POST.get("plan")
        image = request.FILES.get("image")
        pdf = request.FILES.get("pdf")

        course = Course(
            plan=plan,
            title=title,
            description=des,
            image=image,
            pdf=pdf
        )
        course.save()
        messages.success(request, "Course Created Succesfully!")
        return redirect("admin_course")


@login_required(login_url="admin_login")
def admin_course_update(request, id):
    if request.method == "GET":
        return render(request, "course-update.html")
    else:
        video = request.FILES.get("video")
        course = get_object_or_404(Course, id=id)
        v = Video(
            course=course,
            video=video
        )
        v.save()
        messages.success(request, "Course Updated Succesfully!")
        return redirect("admin_course_update", id)


@login_required(login_url="admin_login")
def admin_logout(request):
    logout(request)
    return redirect("admin_login")


@login_required(login_url="admin_login")
def admin_subsribers(request):
    users = []
    user = User.objects.all()
    for use in user:
        if use.plan == "foundation" or use.plan == "intermediate" or use.plan == "enterprise":
            users.append(use)
    
    context = {
        "users": users
    }

    return render(request, "admin-sub.html", context)


@login_required(login_url="admin_login")
def admin_subsribers_cancel(request, id):
    user = get_object_or_404(User, id = id)
    user.plan = None
    user.save()

    return redirect('admin_subsribers')


@login_required(login_url="admin_login")
def admin_subsribers_search(request):
    email = request.GET.get("email")
    users = User.objects.filter(email=email)
    context = {
        "users": users
    }

    return render(request, "admin-sub.html", context)
    





# em3574.rasheed.com
# u16966424.wl175.sendgrid.net
# s1.domainkey.u16966424.wl175.sendgrid.net
# s2.domainkey.u16966424.wl175.sendgrid.net
# s1._domainkey.rasheed.com
# s2._domainkey.rasheed.com


# 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 