from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import (
    AuthenticationView,
    delete_film,
    like_film,
    # MainView,
    main_page,
    profile_page,
    SignupView,
    AddFilmView,
    # FilmDetailView,
    FilmDetail,
    logout_page,
    # about,
    # cart,
    # contact,
    # privacy,
    # ShopView,
    # blog,
    # CreateAddressView,
    # AddressView,
    # process_order,
)

urlpatterns = [
    path("", main_page, name="main_page"),
    path("profile/", profile_page, name="profile_page"),
    path("add_film/", AddFilmView.as_view(), name="add_film"),
    path('film/<slug:slug>/delete/', delete_film, name='delete_film'),
    path("film/<slug:slug>/", FilmDetail, name="film_detail"),
    path('like_film/', like_film, name='like_film'),
    # path("about/", about, name="about_page"),
    # path("cart/", cart, name="cart_page"),
    # path("contact/", contact, name="contact_page"),
    # path("privacy", privacy, name="privacy_page"),
    # path("shop/", ShopView.as_view(), name="shop_page"),
    # path("blog/", blog, name="blog_page"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", AuthenticationView.as_view(), name="login"),
    path("logout/", logout_page, name="logout"),
    # path("address/", AddressView.as_view(), name="address-list"),
    # path("address/create/", CreateAddressView.as_view(), name="address_new"),
    # path("process_order/", process_order, name="process_order"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
