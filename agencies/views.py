from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from .models import Agency, Resource, EmergencyAlert, UserProfile
from .forms import AgencyRegistrationForm, ResourceForm, UserRegistrationForm

def landing(request):
    return render(request, 'agencies/landing.html')

def agency_list(request):
    agencies = Agency.objects.all()
    return render(request, 'agencies/agency_list.html', {'agencies': agencies})

def agency_register(request):
    if request.method == 'POST':
        form = AgencyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agency_list')
    else:
        form = AgencyRegistrationForm()
    return render(request, 'agencies/agency_register.html', {'form': form})

from django.contrib import messages

def register(request):
    from .models import Agency
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create UserProfile
            agency = form.cleaned_data.get('agency')
            role = 'agency_user'
            UserProfile.objects.create(user=user, agency=agency, role=role)
            # Add success message
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
        else:
            # Add error message for invalid form
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    agencies = Agency.objects.all()
    return render(request, 'registration/register.html', {'form': form, 'agencies': agencies})

from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('landing')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('landing')

def is_admin(user):
    return hasattr(user, 'profile') and user.profile.role == 'admin'

def is_agency_user(user):
    return hasattr(user, 'profile') and user.profile.role == 'agency_user'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    agency_count = Agency.objects.count()
    resource_count = Resource.objects.aggregate(total=Count('id'))['total']
    active_alerts_count = EmergencyAlert.objects.filter(active=True).count()

    # Example data for charts: alerts per day for last 7 days
    today = now().date()
    seven_days_ago = today - timedelta(days=6)
    alerts_per_day = (
        EmergencyAlert.objects.filter(created_at__date__gte=seven_days_ago)
        .annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    # Prepare data for chart.js
    chart_labels = [alert['day'].strftime('%Y-%m-%d') for alert in alerts_per_day]
    chart_data = [alert['count'] for alert in alerts_per_day]

    context = {
        'agency_count': agency_count,
        'resource_count': resource_count,
        'active_alerts_count': active_alerts_count,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'agencies/admin_dashboard.html', context)

def agency_detail(request, pk):
    return render(request, 'agencies/agency_detail.html')

def resource_list(request):
    resources = Resource.objects.select_related('agency').all()
    return render(request, 'agencies/resource_list.html', {'resources': resources})

def emergency_alerts(request):
    disaster_type = request.GET.get('disaster_type')
    location = request.GET.get('location')

    alerts = EmergencyAlert.objects.filter(active=True)

    if disaster_type:
        alerts = alerts.filter(title__icontains=disaster_type)
    if location:
        alerts = alerts.filter(description__icontains=location)

    alerts = alerts.order_by('-created_at')
    return render(request, 'agencies/emergency_alerts.html', {'alerts': alerts})

from django.shortcuts import get_object_or_404

# Removed duplicate register view that only rendered template without form handling

def chat(request):
    return render(request, 'agencies/chat.html')

def map_view(request):
    return render(request, 'agencies/map.html')

from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils.timezone import now, timedelta

def admin_dashboard(request):
    agency_count = Agency.objects.count()
    resource_count = Resource.objects.aggregate(total=Count('id'))['total']
    active_alerts_count = EmergencyAlert.objects.filter(active=True).count()

    # Example data for charts: alerts per day for last 7 days
    today = now().date()
    seven_days_ago = today - timedelta(days=6)
    alerts_per_day = (
        EmergencyAlert.objects.filter(created_at__date__gte=seven_days_ago)
        .annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    # Prepare data for chart.js
    chart_labels = [alert['day'].strftime('%Y-%m-%d') for alert in alerts_per_day]
    chart_data = [alert['count'] for alert in alerts_per_day]

    context = {
        'agency_count': agency_count,
        'resource_count': resource_count,
        'active_alerts_count': active_alerts_count,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'agencies/admin_dashboard.html', context)

def disaster_info(request, disaster_type):
    disaster_type = disaster_type.lower()
    valid_disasters = ['earthquake', 'tsunami', 'flood', 'fire']
    if disaster_type not in valid_disasters:
        return render(request, 'agencies/disaster_not_found.html', status=404)
    return render(request, f'agencies/disasters/{disaster_type}.html')

from .forms import ResourceForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def resource_create(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('resource_list'))
    else:
        form = ResourceForm()
    return render(request, 'agencies/resource_form.html', {'form': form, 'title': 'Add Resource'})

def resource_update(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('resource_list'))
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'agencies/resource_form.html', {'form': form, 'title': 'Edit Resource'})

def resource_delete(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        resource.delete()
        return HttpResponseRedirect(reverse('resource_list'))
    return render(request, 'agencies/resource_confirm_delete.html', {'resource': resource})
