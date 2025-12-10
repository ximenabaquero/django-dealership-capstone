# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
import logging
import json
from django.views.decorators.csrf import csrf_exempt
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            username = body.get("userName")
            password = body.get("password")
        except Exception:
            return JsonResponse({"status": "Invalid JSON"}, status=400)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse(
                {"userName": username, "status": "Authenticated"},
                status=200
            )
        else:
            return JsonResponse({"status": "Invalid credentials"}, status=401)

    return JsonResponse({"status": "Bad request"}, status=400)


@csrf_exempt
def logout_user(request):
    if request.method == "GET":
        logout(request)          # Destroy session
        data = {"userName": ""}  # Return empty username
        return JsonResponse(data, status=200)

    return JsonResponse({"status": "Bad request"}, status=400)
