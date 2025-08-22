# Generated migration for updated Favorito model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_favorito'),
    ]

    operations = [
        # Create new table with updated structure
        migrations.CreateModel(
            name='FavoritoContenido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido_id', models.CharField(max_length=100)),
                ('contenido_titulo', models.CharField(max_length=255)),
                ('tipo_contenido', models.CharField(choices=[('anime', 'Anime'), ('libro', 'Libro')], max_length=10)),
                ('autor', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_agregado', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favoritos_nuevos', to='app.usuario')),
            ],
            options={
                'verbose_name': 'Favorito',
                'verbose_name_plural': 'Favoritos',
                'db_table': 'favoritos_contenido',
            },
        ),
        
        # Add unique constraint
        migrations.AlterUniqueTogether(
            name='favoritocontenido',
            unique_together={('usuario', 'contenido_id', 'tipo_contenido')},
        ),
    ]
