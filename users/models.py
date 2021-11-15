# import binascii
# import os
# import hashlib
#
# from django.db import models
# from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.models import User
#
# class TestToken(models.Model):
#     key = models.CharField(_("Key"), max_length=40, primary_key=True)
#     user = models.OneToOneField(
#         User,
#         related_name='auth_token',
#         on_delete=models.CASCADE,
#         verbose_name=_("User")
#     )
#     created = models.DateTimeField(_("Created"), auto_now_add=True)
#
#     class Meta:
#         verbose_name = _("Token")
#         verbose_name_plural = _("Tokens")
#
#     def save(self, *args, **kwargs):
#         self.key = hashlib.sha256(
#             self.generate_key().encode()
#         )
#         return super().save(*args, **kwargs)
#
#     @classmethod
#     def generate_key(cls):
#         return binascii.hexlify(os.urandom(20)).decode()
#
#     def __str__(self):
#         return self.key
