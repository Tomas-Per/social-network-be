# Generated by Django 4.1.7 on 2023-04-01 13:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("post", "0002_postvote_commentvote"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="commentvote",
            options={"verbose_name": "Comment vote", "verbose_name_plural": "Comment votes"},
        ),
        migrations.AlterModelOptions(
            name="postvote",
            options={"verbose_name": "Post vote", "verbose_name_plural": "Post votes"},
        ),
        migrations.AlterUniqueTogether(
            name="commentvote",
            unique_together={("user", "comment")},
        ),
        migrations.AlterUniqueTogether(
            name="postvote",
            unique_together={("user", "post")},
        ),
    ]
