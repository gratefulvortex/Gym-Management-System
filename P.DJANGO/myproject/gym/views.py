from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import MembershipForm
from .models import Member, Membership, Attendance
from django.contrib import messages
from django.db.models import Max
from datetime import datetime
from django.http import HttpResponseRedirect
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers

# Define your view functions
def welcome_page(request):
    return render(request, 'welcome.html')

@cache_control(max_age=3600)  # Set the cache to expire after 1 hour (adjust as needed)
@vary_on_headers('User-Agent')
def index(request):
    return render(request, 'index.html')

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@vary_on_headers('User-Agent')
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/welcome/')  # Redirect to a new URL after successful form submission
        else:
            return render(request, 'login.html', {'message': 'Incorrect username or password'})
    else:
        return render(request, 'login.html')

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@vary_on_headers('User-Agent')
def register_page(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        new_password = request.POST.get('new_password')
        # Check if the username already exists
        if User.objects.filter(username=new_username).exists():
            return render(request, 'login.html', {'message': 'Username already exists. Please choose a different one.'})
        else:
            # Create a new user
            user = User.objects.create_user(username=new_username, password=new_password)
            user.save()
            return render(request, 'login.html', {'message': 'Registration successful. Please log in.'})
    else:
        return redirect('login')  # Redirect to login page if user accesses register page directly

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@vary_on_headers('User-Agent')
def membership_page(request):
    if request.method == 'POST':
        form = MembershipForm(request.POST)
        if form.is_valid():
            # Count the existing members to determine the unique number for the new member
            max_unique_number = Member.objects.aggregate(Max('unique_number'))['unique_number__max'] or 0
            new_unique_number = max_unique_number + 1
            
            # Save the form data
            membership = form.save(commit=False)
            membership.save()

            # Create a new Member instance with the assigned unique number and tenure from the form
            member = Member.objects.create(
                name=membership.name,
                membership_plan=membership.membership_plan,
                unique_number=new_unique_number,
                tenure=form.cleaned_data['tenure'],  # Assign tenure from the form
                start_date=membership.start_date,  # Assign start date from the form
                end_date=membership.end_date  # Assign end date from the form
            )
            
            # Add a success message
            messages.success(request, 'New member added successfully.')
            
            # Clear the form fields by initializing a new form instance
            form = MembershipForm()
        else:
            # If form is invalid, show error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = MembershipForm()
    return render(request, 'add_membership.html', {'form': form})

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@vary_on_headers('User-Agent')
def members_page(request):
    # Retrieve the membership plan selected by the user (if any)
    membership_plan = request.GET.get('membership_plan')

    # Filter members based on the selected membership plan
    if membership_plan:
        members = Member.objects.filter(membership_plan=membership_plan)
    else:
        members = Member.objects.all()  # Retrieve all members if no plan is selected

    return render(request, 'members.html', {'members': members})
      

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@vary_on_headers('User-Agent')
def take_attendance_page(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')

        if member_id:  # If a member ID is provided, display attendance records for that member
            try:
                member = Member.objects.get(unique_number=member_id)
                
                # Retrieve all attendance records for the specific member
                member_attendance_records = Attendance.objects.filter(member=member)

                entry_time = datetime.now()
                # Add new attendance record
                new_attendance_record = Attendance.objects.create(member=member, entry_time=entry_time)
                
                # Prepare message to display in template
                message = f"Thank you, {member.name}. Your entry time has been recorded as {entry_time.strftime('%Y-%m-%d %H:%M:%S')}"

            except Member.DoesNotExist:
                message = "Invalid member ID. Please enter a valid ID."
                member_attendance_records = None
        else:  # If no member ID is provided, display attendance records for all members
            message = None
            member_attendance_records = None

        all_attendance_records = Attendance.objects.all()  # Retrieve all attendance records for all members

    else:
        message = None
        member_attendance_records = None
        all_attendance_records = Attendance.objects.all()

    return render(request, 'take_attendance.html', {'message': message, 'member_attendance_records': member_attendance_records, 'all_attendance_records': all_attendance_records})

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@vary_on_headers('User-Agent')
def employee_page(request):
    return render(request, 'employee.html')

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@vary_on_headers('User-Agent')
def logout_view(request):
    logout(request)
    return redirect('login')  # Assuming your login page URL is named 'login'
