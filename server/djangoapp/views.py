from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import json
import os

# ---------------- AUTH ----------------

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        body = json.loads(request.body)
        user = authenticate(
            username=body.get("userName"),
            password=body.get("password")
        )
        if user:
            login(request, user)
            return JsonResponse({"status": "Authenticated", "userName": user.username})
        return JsonResponse({"status": "Invalid credentials"}, status=401)

    return JsonResponse({"status": "Bad request"}, status=400)


@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def register_user(request):
    body = json.loads(request.body)
    if User.objects.filter(username=body["userName"]).exists():
        return JsonResponse({"status": False, "error": "Already Registered"})

    user = User.objects.create_user(
        username=body["userName"],
        password=body["password"],
        first_name=body.get("firstName", ""),
        last_name=body.get("lastName", ""),
        email=body.get("email", "")
    )
    login(request, user)
    return JsonResponse({"status": True, "userName": user.username})


def _spa_index(request):
    return TemplateView.as_view(template_name="index.html")(request)


@csrf_exempt
def login_route(request):
    if request.method == "POST":
        return login_user(request)
    return _spa_index(request)


@csrf_exempt
def register_route(request):
    if request.method == "POST":
        return register_user(request)
    return _spa_index(request)


# ---------------- DEALERS ----------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "database", "data")
DEALERS_FILE = os.path.join(DATA_DIR, "dealerships.json")


def load_dealers():
    with open(DEALERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["dealerships"]


def get_dealers(request, state=None):
    dealers = load_dealers()

    normalized = []
    for d in dealers:
        normalized.append({
            "id": d["id"],
            "full_name": d["full_name"],
            "city": d["city"],
            "address": d["address"],
            "zip": d["zip"],
            "state": d["state"],
        })

    if state and state != "All":
        normalized = [x for x in normalized if x["state"] == state]

    return JsonResponse({"status": 200, "dealers": normalized})


def get_dealer(request, dealer_id):
    dealers = load_dealers()
    dealer = next(d for d in dealers if d["id"] == dealer_id)
    return JsonResponse({"status": 200, "dealer": dealer})
