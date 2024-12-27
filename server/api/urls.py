from django.urls import include, path

urlpatterns = [
    path("account/", include("account.urls")),
    path("discount/", include("discount.urls")),
    path("product/", include("product.urls")),
    path("orderdetail/", include("orderdetail.urls")),
    path("order/", include("order.urls")),
    path("review/", include("review.urls")),
    path("reply/", include("reply.urls")),
]