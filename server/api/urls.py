from django.urls import include, path

urlpatterns = [
    path("account/", include("account.urls")),
    path("discount/", include("discount.urls")),
    path("cart/", include("cart.urls")),
]