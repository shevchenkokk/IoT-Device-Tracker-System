from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import SignUpForm, LoginForm, PasswordResetForm
from .forms import DevicesGroupAddForm, DevicesGroupEditForm
from .forms import DeviceAddForm, DeviceEditForm
from .mqtt_client import MQTTClient, mqtt_clients
from .models import User, DeviceGroup, Device
from .models import Parameter, SentData, DataFrame
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.contrib.auth import authenticate, login as user_login
from django.contrib.auth import logout as user_logout
from datetime import datetime
import hashlib
import pickle

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'InfoSystem/base.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            salt = get_random_string(length=128)
            hashed_password = make_password(password=password1, salt=salt)
            user = User.objects.create(username=username, \
                                        password=hashed_password, \
                                        email=email, \
                                        salt=salt)    
            user.save()
            mqtt_client = MQTTClient(str(user.user_id), user.username, user.password)
            mqtt_client.connect_to_mqtt()
            mqtt_client.client.loop_start()
            mqtt_clients[user.user_id] = mqtt_client
            user_login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    content = {
        'form': form,
    }
    return render(request, 'InfoSystem/sign-up.html', content)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.get(username=username)
            user_login(request, user)
            return redirect('profile')
    else:
        form = LoginForm()
    content = {
        'form': form,
    }
    return render(request, 'InfoSystem/auth.html', content)

def profile(request):
    return render(request, 'InfoSystem/profile.html')

def logout(request):
    user_logout(request)
    return redirect('home')

def password_reset(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
    else:
        form = PasswordResetForm()
    content = {
        'form': form,
    }
    return render(request, 'InfoSystem/password_reset.html', content)

def add_group(request):
    if request.method == 'POST':
        form = DevicesGroupAddForm(request.POST)
        if form.is_valid():
            device_group_name = form.cleaned_data['device_group_name']
            description = form.cleaned_data['description']
            status = 'active'
            creation_date = datetime.now()
            device_group = DeviceGroup.objects.create(device_group_name=device_group_name, \
                                        creation_date=creation_date, \
                                        status=status, \
                                        user=request.user, \
                                        description=description)
            device_group.save()
            return redirect('groups')
    else:
        form = DevicesGroupAddForm()
    content = {
        'form': form,
    }
    return render(request, 'InfoSystem/add-group.html', content)

def groups(request):
    groups = DeviceGroup.objects.filter(user=request.user).order_by('-creation_date')
    search_input = request.GET.get('search') or ''
    if search_input:
        groups = DeviceGroup.objects.filter(user=request.user, \
                                                  device_group_name__istartswith=search_input).order_by('-creation_date')
    content = {
        'search_input': search_input,
        'groups': groups,
    }
    return render(request, 'InfoSystem/groups.html', content)

def edit_group(request, device_group_id):
    group = get_object_or_404(DeviceGroup, device_group_id=device_group_id)
    if request.method == 'POST':
        form = DevicesGroupEditForm(request.POST)
        if form.is_valid():
            device_group_name = form.cleaned_data['device_group_name']
            description = form.cleaned_data['description']
            group.device_group_name = device_group_name
            group.description = description
            group.save()
            return redirect ('groups')
    else:
        form = DevicesGroupEditForm()
    content = {
        'form': form,
        'group': group,
    }
    return render(request, 'InfoSystem/edit-group.html', content)

def delete_group(request, device_group_id):
    group = get_object_or_404(DeviceGroup, device_group_id=device_group_id)
    if request.method == 'POST':
        group.delete()
        return redirect ('groups')
    return render(request, 'InfoSystem/delete-group.html', {'group': group})

def show_group(request, device_group_id):
    group = get_object_or_404(DeviceGroup, device_group_id=device_group_id)
    devices = Device.objects.filter(device_group_id=group.device_group_id).order_by('-creation_date')
    search_input = request.GET.get('search') or ''
    if search_input:
        devices = Device.objects.filter(device_group_id=device_group_id, \
                                        device_name__istartswith=search_input).order_by('-creation_date')
    content = {
        'group': group,
        'devices': devices,
        'search_input': search_input,
    }
    return render(request, 'InfoSystem/show-group.html', content)

def add_device(request, device_group_id):
    group = get_object_or_404(DeviceGroup, device_group_id=device_group_id)
    if request.method == 'POST':
        form = DeviceAddForm(request.POST)
        if form.is_valid():
            device_name = form.cleaned_data['device_name']
            location_name = form.cleaned_data['location_name']
            description = form.cleaned_data['description']
            creation_date = datetime.now()
            status = 'active'
            device = Device.objects.create(device_name=device_name, \
                                        creation_date=creation_date, \
                                        status=status, \
                                        device_group_id=group.device_group_id, \
                                        location_name=location_name, \
                                        description=description)
            device.save()
            token_prep = (str(device.device_id) + get_random_string(32)).encode('utf-8')
            authentication_token = hashlib.sha256(token_prep).hexdigest()
            device.authentication_token = authentication_token
            device.save()
            #MQTT
            topic_sub = group.device_group_name + '/devices/' + str(device.device_id) + '/telemetry' 
            mqtt_clients[group.user.user_id].subscribe(topic_sub)
            content = {
                'group': group,
                'device': device,
                'auth_token': token_prep,
            }
            return render(request, 'InfoSystem/show-device-token.html', content)
            # return redirect('show-group', group.info_system_id)
    else:
        form = DeviceAddForm()
    content = {
        'form': form,
        'group': group,
    }
    return render(request, 'InfoSystem/add-device.html', content)

def show_device(request, device_group_id, device_id):
    group = get_object_or_404(DeviceGroup, device_group_id=device_group_id)
    device = get_object_or_404(Device, device_id=device_id)
    parameters = Parameter.objects.filter(device_id=device_id)
    parameter_ids = [parameter.parameter_id for parameter in parameters]
    data_frames = DataFrame.objects.filter(parameter_id__in=parameter_ids)
    content = {
        'group': group,
        'device': device,
        'data_frames': data_frames,
    }
    return render(request, 'InfoSystem/show-device.html', content)

def edit_device(request, device_group_id, device_id):
    group = get_object_or_404(DeviceGroup, device_group_id=device_group_id)
    device = get_object_or_404(Device, device_id=device_id)
    if request.method == 'POST':
        form = DeviceEditForm(request.POST)
        if form.is_valid():
            device_name = form.cleaned_data['device_name']
            description = form.cleaned_data['description']
            device.device_name = device_name
            device.description = description
            device.save()
            return redirect ('show-group', group.device_group_id)
    else:
        form = DeviceEditForm()
    content = {
        'form': form,
        'group': group,
        'device': device,
    }
    return render(request, 'InfoSystem/edit-device.html', content)

def delete_device(request, device_group_id, device_id):
    group = get_object_or_404(DeviceGroup, device_group_id=device_group_id)
    device = get_object_or_404(Device, device_id=device_id)
    if request.method == 'POST':
        device.delete()
        return redirect('show-group', device_group_id)
    content = {
        'group': group,
        'device': device,
    }
    return render(request, 'InfoSystem/delete-device.html', content)

def show_device_token(request, device_group_id, device_id):
    group = get_object_or_404(DeviceGroup, device_group_id=device_group_id)
    device = get_object_or_404(Device, device_id=device_id)
    content = {
        'group': group,
        'device': device,
    }
    return render(request, 'InfoSystem/show-device-token.html', content)