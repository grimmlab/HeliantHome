# Generated by Django 3.2.4 on 2021-06-22 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accession',
            fields=[
                ('accession_id', models.CharField(db_index=True, max_length=20, primary_key=True, serialize=False)),
                ('ppn', models.CharField(blank=True, db_index=True, max_length=20, null=True)),
                ('pit', models.CharField(blank=True, db_index=True, max_length=20, null=True)),
                ('aclass', models.CharField(blank=True, db_index=True, max_length=20, null=True)),
                ('name', models.CharField(blank=True, db_index=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, max_length=100, null=True)),
                ('lastname', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClimateVariable',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ClimateVariableValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('climate_variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.climatevariable')),
            ],
        ),
        migrations.CreateModel(
            name='Individual',
            fields=[
                ('individual_id', models.CharField(db_index=True, max_length=20, primary_key=True, serialize=False)),
                ('genotype_id', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OntologyTerm',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Phenotype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('type', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Quantitative'), (1, 'Categorical'), (2, 'Binary')], db_index=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('method', models.TextField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_category', models.CharField(blank=True, max_length=255, null=True)),
                ('shapiro_test_statistic', models.FloatField(blank=True, null=True)),
                ('shapiro_p_value', models.FloatField(blank=True, null=True)),
                ('integration_date', models.DateTimeField(auto_now_add=True)),
                ('easygwas_link', models.CharField(blank=True, max_length=500, null=True)),
                ('ontology', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.ontologyterm')),
            ],
        ),
        migrations.CreateModel(
            name='PhenotypeLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accession', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.accession')),
                ('individual', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.individual')),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_order', models.TextField()),
                ('publication_tag', models.CharField(blank=True, max_length=255, null=True)),
                ('pub_year', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('journal', models.CharField(max_length=255)),
                ('volume', models.CharField(blank=True, max_length=255, null=True)),
                ('pages', models.CharField(blank=True, max_length=255, null=True)),
                ('doi', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('pubmed_id', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('authors', models.ManyToManyField(blank=True, to='main.Author')),
            ],
        ),
        migrations.CreateModel(
            name='SoilVariable',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('update_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('publications', models.ManyToManyField(blank=True, to='main.Publication')),
            ],
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ncbi_id', models.IntegerField(blank=True, null=True)),
                ('species', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('species_image', models.CharField(blank=True, max_length=255, null=True)),
                ('cultivated', models.BooleanField(default=False)),
                ('study', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.study')),
            ],
        ),
        migrations.CreateModel(
            name='SoilVariableValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('soil_variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.soilvariable')),
            ],
        ),
        migrations.CreateModel(
            name='Population',
            fields=[
                ('population_id', models.CharField(db_index=True, max_length=20, primary_key=True, serialize=False)),
                ('voucher_number', models.CharField(blank=True, max_length=20, null=True)),
                ('herbarium', models.CharField(blank=True, max_length=20, null=True)),
                ('individuals_sampled', models.IntegerField(blank=True, null=True)),
                ('collection_date', models.DateTimeField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('sitename', models.TextField(blank=True, null=True)),
                ('elevation', models.IntegerField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, db_index=True, null=True)),
                ('latitude', models.FloatField(blank=True, db_index=True, null=True)),
                ('location_description', models.TextField(blank=True, null=True)),
                ('ecology_description', models.TextField(blank=True, null=True)),
                ('woody_plant', models.TextField(blank=True, null=True)),
                ('pop_size_est', models.IntegerField(blank=True, null=True)),
                ('climate_variables', models.ManyToManyField(blank=True, to='main.ClimateVariableValue')),
                ('soil_variables', models.ManyToManyField(blank=True, to='main.SoilVariableValue')),
                ('species', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.species')),
            ],
        ),
        migrations.CreateModel(
            name='PlantImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255)),
                ('thumb_filename', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=500)),
                ('accession', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.accession')),
                ('individual', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.individual')),
                ('study', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.study')),
            ],
        ),
        migrations.CreateModel(
            name='PhenotypeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('phenotype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.phenotype')),
                ('phenotype_link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.phenotypelink')),
            ],
        ),
        migrations.AddField(
            model_name='phenotypelink',
            name='study',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.study'),
        ),
        migrations.AddField(
            model_name='phenotype',
            name='species',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.species'),
        ),
        migrations.AddField(
            model_name='phenotype',
            name='study',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.study'),
        ),
        migrations.AddField(
            model_name='individual',
            name='population',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.population'),
        ),
        migrations.AddField(
            model_name='individual',
            name='species',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.species'),
        ),
        migrations.AddField(
            model_name='accession',
            name='population',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.population'),
        ),
        migrations.AddField(
            model_name='accession',
            name='species',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.species'),
        ),
    ]
