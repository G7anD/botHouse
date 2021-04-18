from django.db import models

class BotUser(models.Model):
    user_id = models.PositiveIntegerField("User's tg id", unique=True)
    firstname = models.CharField("first name", max_length=200, blank=True, null=True)
    lastname = models.CharField("last name", max_length=200, blank=True, null=True)
    username = models.CharField("username", max_length=200, blank=True, null=True)
    is_send = models.BooleanField("is send", default=False)
    send_error = models.CharField("send error", max_length=5000, blank=True, null=True)


    # for getting more info
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = 'BotUser'
        verbose_name_plural = 'BotUser'