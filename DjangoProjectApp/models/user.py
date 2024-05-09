from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import Group, Permission

from DjangoProjectApp.models.films import Film


class UserManager(BaseUserManager):
    def create_user(
        self,
        # email,
        username,
        password,
        # phone_number,
        # birthday_date,
                # gender,
    ) -> "User":
        # if not email:
        #     raise ValueError("An email is required.")
        if not password:
            raise ValueError("A password is required.")
        # email = self.normalize_email(email)
        user = self.model(
            # email=email,
            username=username,
            password=password,
            # phone_number=phone_number,
            # birthday_date=birthday_date,
                    # gender=gender,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        # email,
        username,
        password,
        # phone_number,
        # birthday_date,
                # gender,
    ) -> "User":
        # if not email:
        #     raise ValueError("An email is required.")
        if not password:
            raise ValueError("A password is required.")
        # email = self.normalize_email(email)
        user = self.model(
            # email=email,
            username=username,
            password=password,
            # phone_number=phone_number,
            # birthday_date=birthday_date,
                    # gender=gender,
        )
        user.is_superuser = True
        # user.is_staff = True
        user.is_active = True

        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), max_length=15, unique=True)
    likes_lst = models.ManyToManyField(Film, through="Like", through_fields=("user", "film"))
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
    ]

    def get_username(self):
        return f"{self.username}"
    
    @property
    def liked_films(self):
        return Film.objects.filter(likes__user=self)

    def like_film(self, film):
        like = Like.objects.get_or_create(user=self, film=film)
        return like

    def unlike_film(self, film):
        Like.objects.filter(user=self, film=film).delete()

    def has_liked(self, film):
        return Like.objects.filter(user=self, film=film).exists()

    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'film',)