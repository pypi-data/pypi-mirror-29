import unittest
import dbt.main as dbt
import os, shutil
import yaml
import time
import json

from dbt.adapters.factory import get_adapter

from dbt.logger import GLOBAL_LOGGER as logger


DBT_CONFIG_DIR = os.path.abspath(
    os.path.expanduser(os.environ.get("DBT_CONFIG_DIR", '/root/.dbt'))
)

DBT_PROFILES = os.path.join(DBT_CONFIG_DIR, 'profiles.yml')


class FakeArgs(object):
    def __init__(self):
        self.threads = 1
        self.data = False
        self.schema = True
        self.full_refresh = False
        self.models = None
        self.exclude = None


class DBTIntegrationTest(unittest.TestCase):

    prefix = "test{}".format(int(time.time()))

    def postgres_profile(self):
        return {
            'config': {
                'send_anonymous_usage_stats': False
            },
            'test': {
                'outputs': {
                    'default2': {
                        'type': 'postgres',
                        'threads': 4,
                        'host': 'database',
                        'port': 5432,
                        'user': 'root',
                        'pass': 'password',
                        'dbname': 'dbt',
                        'schema': self.unique_schema()
                    },
                    'noaccess': {
                        'type': 'postgres',
                        'threads': 4,
                        'host': 'database',
                        'port': 5432,
                        'user': 'noaccess',
                        'pass': 'password',
                        'dbname': 'dbt',
                        'schema': self.unique_schema()
                    }
                },
                'target': 'default2'
            }
        }

    def snowflake_profile(self):
        return {
            'config': {
                'send_anonymous_usage_stats': False
            },
            'test': {
                'outputs': {
                    'default2': {
                        'type': 'snowflake',
                        'threads': 4,
                        'account': os.getenv('SNOWFLAKE_TEST_ACCOUNT'),
                        'user': os.getenv('SNOWFLAKE_TEST_USER'),
                        'password': os.getenv('SNOWFLAKE_TEST_PASSWORD'),
                        'database': os.getenv('SNOWFLAKE_TEST_DATABASE'),
                        'schema': self.unique_schema(),
                        'warehouse': os.getenv('SNOWFLAKE_TEST_WAREHOUSE'),
                    },
                    'noaccess': {
                        'type': 'snowflake',
                        'threads': 4,
                        'account': os.getenv('SNOWFLAKE_TEST_ACCOUNT'),
                        'user': 'noaccess',
                        'password': 'password',
                        'database': os.getenv('SNOWFLAKE_TEST_DATABASE'),
                        'schema': self.unique_schema(),
                        'warehouse': os.getenv('SNOWFLAKE_TEST_WAREHOUSE'),
                    }
                },
                'target': 'default2'
            }
        }

    def bigquery_profile(self):
        credentials_json_str = os.getenv('BIGQUERY_SERVICE_ACCOUNT_JSON').replace("'", '')
        credentials = json.loads(credentials_json_str)
        project_id = credentials.get('project_id')

        return {
            'config': {
                'send_anonymous_usage_stats': False
            },
            'test': {
                'outputs': {
                    'default2': {
                        'type': 'bigquery',
                        'method': 'service-account-json',
                        'threads': 1,
                        'project': project_id,
                        'keyfile_json': credentials,
                        'schema': self.unique_schema(),
                    },
                },
                'target': 'default2'
            }
        }

    def unique_schema(self):
        schema =  self.schema
        return "{}_{}".format(self.prefix, schema)

    def get_profile(self, adapter_type):
        if adapter_type == 'postgres':
            return self.postgres_profile()
        elif adapter_type == 'snowflake':
            return self.snowflake_profile()
        elif adapter_type == 'bigquery':
            return self.bigquery_profile()

    def setUp(self):
        # create a dbt_project.yml

        base_project_config = {
            'name': 'test',
            'version': '1.0',
            'test-paths': [],
            'source-paths': [self.models],
            'profile': 'test'
        }

        project_config = {}
        project_config.update(base_project_config)
        project_config.update(self.project_config)

        with open("dbt_project.yml", 'w') as f:
            yaml.safe_dump(project_config, f, default_flow_style=True)

        # create profiles

        profile_config = {}
        default_profile_config = self.postgres_profile()
        profile_config.update(default_profile_config)
        profile_config.update(self.profile_config)

        if not os.path.exists(DBT_CONFIG_DIR):
            os.makedirs(DBT_CONFIG_DIR)

        with open(DBT_PROFILES, 'w') as f:
            yaml.safe_dump(profile_config, f, default_flow_style=True)

        target = profile_config.get('test').get('target')

        if target is None:
            target = profile_config.get('test').get('run-target')

        profile = profile_config.get('test').get('outputs').get(target)

        adapter = get_adapter(profile)

        # it's important to use a different connection handle here so
        # we don't look into an incomplete transaction
        adapter.cleanup_connections()
        connection = adapter.acquire_connection(profile, '__test')
        self.handle = connection.get('handle')
        self.adapter_type = profile.get('type')
        self.profile = profile

        if self.adapter_type == 'bigquery':
            schema_name = self.unique_schema()
            adapter.drop_schema(profile, schema_name, '__test')
            adapter.create_schema(profile, schema_name, '__test')
        else:
            self.run_sql('DROP SCHEMA IF EXISTS "{}" CASCADE'.format(self.unique_schema()))
            self.run_sql('CREATE SCHEMA "{}"'.format(self.unique_schema()))

    def use_default_project(self, overrides=None):
        # create a dbt_project.yml
        base_project_config = {
            'name': 'test',
            'version': '1.0',
            'test-paths': [],
            'source-paths': [self.models],
            'profile': 'test',
        }

        project_config = {}
        project_config.update(base_project_config)
        project_config.update(self.project_config)
        project_config.update(overrides or {})

        with open("dbt_project.yml", 'w') as f:
            yaml.safe_dump(project_config, f, default_flow_style=True)

    def use_profile(self, adapter_type):
        profile_config = {}
        default_profile_config = self.get_profile(adapter_type)

        profile_config.update(default_profile_config)
        profile_config.update(self.profile_config)

        if not os.path.exists(DBT_CONFIG_DIR):
            os.makedirs(DBT_CONFIG_DIR)

        with open(DBT_PROFILES, 'w') as f:
            yaml.safe_dump(profile_config, f, default_flow_style=True)

        profile = profile_config.get('test').get('outputs').get('default2')
        adapter = get_adapter(profile)

        # it's important to use a different connection handle here so
        # we don't look into an incomplete transaction
        connection = adapter.acquire_connection(profile, '__test')
        self.handle = connection.get('handle')
        self.adapter_type = profile.get('type')
        self.profile = profile

        if self.adapter_type == 'bigquery':
            adapter.drop_schema(profile, self.unique_schema(), '__test')
            adapter.create_schema(profile, self.unique_schema(), '__test')
        else:
            self.run_sql('DROP SCHEMA IF EXISTS "{}" CASCADE'.format(self.unique_schema()))
            self.run_sql('CREATE SCHEMA "{}"'.format(self.unique_schema()))

    def tearDown(self):
        os.remove(DBT_PROFILES)
        os.remove("dbt_project.yml")

        # quick fix for windows bug that prevents us from deleting dbt_modules
        try:
            if os.path.exists('dbt_modules'):
                shutil.rmtree('dbt_modules')
        except:
            os.rename("dbt_modules", "dbt_modules-{}".format(time.time()))

        if self.adapter_type == 'bigquery':
            adapter = get_adapter(self.profile)
            adapter.drop_schema(self.profile, self.unique_schema(), '__test')
        else:
            self.run_sql('DROP SCHEMA IF EXISTS "{}" CASCADE'.format(self.unique_schema()))
            self.handle.close()


        # hack for BQ -- TODO
        if hasattr(self.handle, 'close'):
            self.handle.close()

    @property
    def project_config(self):
        return {}

    @property
    def profile_config(self):
        return {}

    def run_dbt(self, args=None, expect_pass=True):
        if args is None:
            args = ["run"]

        args = ["--strict"] + args
        logger.info("Invoking dbt with {}".format(args))

        res, success =  dbt.handle_and_check(args)
        self.assertEqual(success, expect_pass, "dbt exit state did not match expected")

        return res

    def run_dbt_and_check(self, args=None):
        if args is None:
            args = ["run"]

        args = ["--strict"] + args
        logger.info("Invoking dbt with {}".format(args))
        return dbt.handle_and_check(args)

    def run_sql_file(self, path):
        with open(path, 'r') as f:
            statements = f.read().split(";")
            for statement in statements:
                self.run_sql(statement)

    # horrible hack to support snowflake for right now
    def transform_sql(self, query):
        to_return = query

        if self.adapter_type == 'snowflake':
            to_return = to_return.replace("BIGSERIAL", "BIGINT AUTOINCREMENT")

        to_return = to_return.format(schema=self.unique_schema())

        return to_return

    def run_sql(self, query, fetch='None'):
        if query.strip() == "":
            return

        with self.handle.cursor() as cursor:
            try:
                cursor.execute(self.transform_sql(query))
                self.handle.commit()
                if fetch == 'one':
                    return cursor.fetchone()
                elif fetch == 'all':
                    return cursor.fetchall()
                else:
                    return
            except BaseException as e:
                self.handle.rollback()
                print(query)
                print(e)
                raise e

    def get_table_columns(self, table, schema=None):
        schema = self.unique_schema() if schema is None else schema
        sql = """
                select column_name, data_type, character_maximum_length
                from information_schema.columns
                where table_name = '{}'
                and table_schema = '{}'
                order by column_name asc"""

        result = self.run_sql(sql.format(table, schema), fetch='all')

        return result

    def get_models_in_schema(self, schema=None):
        schema = self.unique_schema() if schema is None else schema
        sql = """
                select table_name,
                        case when table_type = 'BASE TABLE' then 'table'
                             when table_type = 'VIEW' then 'view'
                             else table_type
                        end as materialization
                from information_schema.tables
                where table_schema = '{}'
                order by table_name
                """

        result = self.run_sql(sql.format(schema), fetch='all')

        return {model_name: materialization for (model_name, materialization) in result}

    def assertTablesEqual(self, table_a, table_b, table_a_schema=None, table_b_schema=None):
        table_a_schema = self.unique_schema() if table_a_schema is None else table_a_schema
        table_b_schema = self.unique_schema() if table_b_schema is None else table_b_schema

        self.assertTableColumnsEqual(table_a, table_b, table_a_schema, table_b_schema)
        self.assertTableRowCountsEqual(table_a, table_b, table_a_schema, table_b_schema)

        columns = self.get_table_columns(table_a, table_a_schema)
        columns_csv = ", ".join(['"{}"'.format(record[0])
                                 for record in columns])
        table_sql = "SELECT {} FROM {}"

        sql = """
            SELECT COUNT(*) FROM (
                (SELECT {columns} FROM "{table_a_schema}"."{table_a}" EXCEPT
                 SELECT {columns} FROM "{table_b_schema}"."{table_b}")
                 UNION ALL
                (SELECT {columns} FROM "{table_b_schema}"."{table_b}" EXCEPT
                 SELECT {columns} FROM "{table_a_schema}"."{table_a}")
            ) AS a""".format(
                columns=columns_csv,
                table_a_schema=table_a_schema,
                table_b_schema=table_b_schema,
                table_a=table_a,
                table_b=table_b
            )

        result = self.run_sql(sql, fetch='one')

        self.assertEquals(
            result[0],
            0,
            sql
        )

    def assertTableRowCountsEqual(self, table_a, table_b, table_a_schema=None, table_b_schema=None):
        table_a_schema = self.unique_schema() if table_a_schema is None else table_a_schema
        table_b_schema = self.unique_schema() if table_b_schema is None else table_b_schema

        table_a_result = self.run_sql('SELECT COUNT(*) FROM "{}"."{}"'.format(table_a_schema, table_a), fetch='one')
        table_b_result = self.run_sql('SELECT COUNT(*) FROM "{}"."{}"'.format(table_b_schema, table_b), fetch='one')

        self.assertEquals(
            table_a_result[0],
            table_b_result[0],
            "Row count of table {} ({}) doesn't match row count of table {} ({})".format(
                table_a,
                table_a_result[0],
                table_b,
                table_b_result[0]
            )
        )

    def assertTableDoesNotExist(self, table, schema=None):
        columns = self.get_table_columns(table, schema)

        self.assertEquals(
            len(columns),
            0
        )

    def assertTableDoesExist(self, table, schema=None):
        columns = self.get_table_columns(table, schema)

        self.assertGreater(
            len(columns),
            0
        )

    def assertTableColumnsEqual(self, table_a, table_b, table_a_schema=None, table_b_schema=None):
        table_a_schema = self.unique_schema() if table_a_schema is None else table_a_schema
        table_b_schema = self.unique_schema() if table_b_schema is None else table_b_schema

        table_a_result = self.get_table_columns(table_a, table_a_schema)
        table_b_result = self.get_table_columns(table_b, table_b_schema)

        self.assertEquals(
            table_a_result,
            table_b_result
        )

    def assertEquals(self, *args, **kwargs):
        # assertEquals is deprecated. This makes the warnings less chatty
        self.assertEqual(*args, **kwargs)
