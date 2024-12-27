from django.urls import include, path

urlpatterns = [
    path("account/", include("account.urls")),
    path("discount/", include("discount.urls")),

    path("product/", include("product.urls")),
]