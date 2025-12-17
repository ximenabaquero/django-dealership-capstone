import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproj.settings")

import django  # noqa: E402

django.setup()

from django.test import Client  # noqa: E402


def main() -> None:
    client = Client()
    host_kw = {"HTTP_HOST": "localhost"}

    resp = client.get("/dealer/15", **host_kw)
    print("GET /dealer/15 ->", resp.status_code, resp.get("Content-Type"))
    print("has_root", b'id="root"' in resp.content)

    resp2 = client.get("/djangoapp/dealer/15", **host_kw)
    j2 = resp2.json()
    print(
        "GET /djangoapp/dealer/15 ->",
        resp2.status_code,
        j2.get("status"),
        "dealer_len",
        len(j2.get("dealer", [])),
    )

    resp3 = client.get("/djangoapp/reviews/dealer/15", **host_kw)
    j3 = resp3.json()
    print(
        "GET /djangoapp/reviews/dealer/15 ->",
        resp3.status_code,
        j3.get("status"),
        "reviews",
        len(j3.get("reviews", [])),
    )


if __name__ == "__main__":
    main()
