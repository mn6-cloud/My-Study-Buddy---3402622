from django.db import migrations, models
from django.utils.text import slugify

def populate_unique_slugs(apps, schema_editor):
    Quiz = apps.get_model('studybuddy', 'Quiz')
    for quiz in Quiz.objects.all():
        base_slug = slugify(quiz.title)
        unique_slug = f"{base_slug}-{quiz.id}"  # Append ID to guarantee uniqueness
        quiz.slug = unique_slug
        quiz.save()

class Migration(migrations.Migration):
    dependencies = [('studybuddy', '0001_initial')]
    
    operations = [
        migrations.AddField(
            model_name='quiz',
            name='slug',
            field=models.SlugField(max_length=100, null=True, unique=False),
        ),
        migrations.RunPython(populate_unique_slugs),
        migrations.AlterField(
            model_name='quiz',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]