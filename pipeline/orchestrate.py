from dagster import job, op
import os

@op
def ingest():
    os.system("python pipeline/ingest.py")
    return True

@op
def validate(context, precedent: bool):
    os.system("python pipeline/validate.py")
    return True

@op
def transform(context, precedent: bool):
    os.system("cd dbt_pipeline && dbt run --profiles-dir .")
    return True

@op
def test_data(context, precedent: bool):
    os.system("cd dbt_pipeline && dbt test --profiles-dir .")
    return True

@job
def ventes_pipeline():
    test_data(transform(validate(ingest())))