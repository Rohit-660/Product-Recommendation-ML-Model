from django.http import JsonResponse
from recommendations.services.redis_client import get_redis

r = get_redis()

def top_buys(request):
    """
    Logged-in user → personalized
    Guest user → global
    """
    user_id = request.GET.get("user_id")

    if user_id:
        data = r.get(f"user:{user_id}:top_buys")
    else:
        data = r.get("global:top_buys")

    products = data.split(",") if data else []

    return JsonResponse({
        "type": "top_buys",
        "products": products
    })


def bought_together(request, product_id):
    # Top 10 highest lift
    data = r.zrevrange(
        f"product:{product_id}:bought_together",
        0,
        9
    )

    return JsonResponse({
        "type": "bought_together",
        "product_id": product_id,
        "products": list(data)
    })
