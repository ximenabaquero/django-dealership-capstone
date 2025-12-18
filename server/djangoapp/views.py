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
CAR_RECORDS_FILE = os.path.join(DATA_DIR, "car_records.json")
REVIEWS_FILE = os.path.join(DATA_DIR, "reviews.json")


def load_dealers():
    with open(DEALERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["dealerships"]


def _load_reviews_payload():
    with open(REVIEWS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_reviews_payload(payload):
    with open(REVIEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def _analyze_sentiment(_text):
    if not _text:
        return "neutral"

    text = str(_text).lower()

    positive_keywords = (
        "fantastic",
        "fantastico",
        "fantasticos",
        "fantástico",
        "fantásticos",
        "great",
        "excellent",
        "amazing",
        "awesome",
        "good",
        "love",
        "perfect",
        "recommend",
    )
    negative_keywords = (
        "bad",
        "terrible",
        "awful",
        "horrible",
        "worst",
        "poor",
        "hate",
        "disappoint",
        "broken",
    )

    if any(k in text for k in positive_keywords):
        return "positive"
    if any(k in text for k in negative_keywords):
        return "negative"
    return "neutral"


def analyze_review(request, review_text):
    sentiment = _analyze_sentiment(review_text)
    return JsonResponse({"sentiment": sentiment})


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


def dealer_detail(request, dealer_id):
    """API used by the React Dealer/PostReview pages: returns dealer as a list."""
    dealers = load_dealers()
    dealer = next((d for d in dealers if d["id"] == dealer_id), None)
    if not dealer:
        return JsonResponse({"status": 404, "dealer": []}, status=404)
    return JsonResponse({"status": 200, "dealer": [dealer]})


def get_reviews_by_dealer(request, dealer_id):
    payload = _load_reviews_payload()
    reviews = [r for r in payload.get("reviews", []) if int(r.get("dealership")) == int(dealer_id)]
    normalized = []
    for r in reviews:
        review_copy = dict(r)
        review_copy["sentiment"] = _analyze_sentiment(review_copy.get("review", ""))
        normalized.append(review_copy)
    return JsonResponse({"status": 200, "reviews": normalized})


def get_cars(request):
    with open(CAR_RECORDS_FILE, "r", encoding="utf-8") as f:
        cars = json.load(f).get("cars", [])

    seen = set()
    car_models = []
    for c in cars:
        make = c.get("make")
        model = c.get("model")
        if not make or not model:
            continue
        key = (make, model)
        if key in seen:
            continue
        seen.add(key)
        car_models.append({"CarMake": make, "CarModel": model})

    car_models.sort(key=lambda x: (x["CarMake"], x["CarModel"]))
    return JsonResponse({"CarModels": car_models})


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse({"status": 405, "error": "Method not allowed"}, status=405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": 400, "error": "Invalid JSON"}, status=400)

    required = ["name", "dealership", "review", "purchase", "purchase_date", "car_make", "car_model", "car_year"]
    missing = [k for k in required if body.get(k) in (None, "")]
    if missing:
        return JsonResponse({"status": 400, "error": f"Missing fields: {', '.join(missing)}"}, status=400)

    payload = _load_reviews_payload()
    reviews = payload.get("reviews", [])
    next_id = (max((int(r.get("id", 0)) for r in reviews), default=0) + 1) if reviews else 1

    new_review = {
        "id": next_id,
        "name": body.get("name"),
        "dealership": int(body.get("dealership")),
        "review": body.get("review"),
        "purchase": bool(body.get("purchase")),
        "purchase_date": body.get("purchase_date"),
        "car_make": body.get("car_make"),
        "car_model": body.get("car_model"),
        "car_year": int(body.get("car_year")),
    }
    reviews.append(new_review)
    payload["reviews"] = reviews
    _save_reviews_payload(payload)

    return JsonResponse({"status": 200, "review": new_review})
