"""
Use this file to configure pluggable app settings and resolve defaults
with any overrides set in project settings.
"""

from django.conf import settings as project_settings


class Settings:
    pass


Settings.AUTH_DECORATOR = getattr(
    project_settings,
    'ELECTIONNIGHT_AUTH_DECORATOR',
    'django.contrib.admin.views.decorators.staff_member_required'
)

Settings.AWS_S3_STATIC_ROOT = getattr(
    project_settings,
    'ELECTIONNIGHT_AWS_S3_STATIC_ROOT',
    'https://www.politico.com/interactives'
)

Settings.SECRET_KEY = getattr(
    project_settings, 'ELECTIONNIGHT_SECRET_KEY', 'a-bad-secret-key')

Settings.AWS_ACCESS_KEY_ID = getattr(
    project_settings, 'ELECTIONNIGHT_AWS_ACCESS_KEY_ID', None)

Settings.AWS_SECRET_ACCESS_KEY = getattr(
    project_settings, 'ELECTIONNIGHT_AWS_SECRET_ACCESS_KEY', None)

Settings.AWS_REGION = getattr(
    project_settings, 'ELECTIONNIGHT_AWS_REGION', None)

Settings.AWS_S3_BUCKET = getattr(
    project_settings, 'ELECTIONNIGHT_AWS_S3_BUCKET', None)

Settings.CLOUDFRONT_ALTERNATE_DOMAIN = getattr(
    project_settings, 'ELECTIONNIGHT_CLOUDFRONT_ALTERNATE_DOMAIN', None)

Settings.S3_UPLOAD_ROOT = getattr(
    project_settings, 'ELECTIONNIGHT_S3_UPLOAD_ROOT', 'uploads/electionnight')


Settings.API_AUTHENTICATION_CLASS = getattr(
    project_settings,
    'ELECTIONNIGHT_API_AUTHENTICATION_CLASS',
    'rest_framework.authentication.BasicAuthentication'
)

Settings.API_PERMISSION_CLASS = getattr(
    project_settings,
    'ELECTIONNIGHT_API_PERMISSION_CLASS',
    'rest_framework.permissions.IsAdminUser'
)

Settings.API_PAGINATION_CLASS = getattr(
    project_settings,
    'ELECTIONNIGHT_API_PAGINATION_CLASS',
    'electionnight.pagination.ResultsPagination'
)

Settings.RESULTS_STATIC_DIR = getattr(
    project_settings, 'ELECTIONNIGHT_RESULTS_STATIC_DIR', 'static_results')

Settings.RESULTS_DAEMON_INTERVAL = getattr(
    project_settings, 'ELECTIONNIGHT_RESULTS_DAEMON_INTERVAL', 20)

Settings.DATABASE_UPLOAD_DAEMON_INTERVAL = getattr(
    project_settings, 'ELECTIONNIGHT_DATABASE_UPLOAD_DAEMON_INTERVAL', 60)

settings = Settings
