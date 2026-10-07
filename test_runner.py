from pathlib import Path
from django.conf import settings
from django.db import connection
from django.test.runner import DiscoverRunner


class SchemaTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        config = super().setup_databases(**kwargs)
        sql = Path(settings.BASE_DIR / "schema.sql").read_text()
        with connection.cursor() as cursor:
            for statement in filter(None, (s.strip() for s in sql.split(";"))):
                cursor.execute(statement)
        return config