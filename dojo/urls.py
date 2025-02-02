from django.conf import settings
from django.urls import re_path
from django.conf.urls import include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as tokenviews
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import HttpResponse
from dojo import views
from dojo.api_v2.views import EndPointViewSet, EngagementViewSet, \
    FindingTemplatesViewSet, FindingViewSet, JiraInstanceViewSet, \
    JiraIssuesViewSet, JiraProjectViewSet, ProductViewSet, CredentialsViewSet, CredentialsMappingViewSet, \
    SLAConfigurationViewset, StubFindingsViewSet, TestImportViewSet, TestsViewSet, TestTypesViewSet, \
    ToolConfigurationsViewSet, ToolProductSettingsViewSet, ToolTypesViewSet, \
    UsersViewSet, ImportScanView, ReImportScanView, ProductTypeViewSet, DojoMetaViewSet, \
    DevelopmentEnvironmentViewSet, NotesViewSet, NoteTypeViewSet, SystemSettingsViewSet, \
    AppAnalysisViewSet, EndpointStatusViewSet, SonarqubeIssueViewSet, SonarqubeIssueTransitionViewSet, \
    RegulationsViewSet, ProductTypeMemberViewSet, ProductMemberViewSet, RiskAcceptanceViewSet, \
    DojoGroupViewSet, ProductGroupViewSet, ProductTypeGroupViewSet, RoleViewSet, GlobalRoleViewSet, \
    DojoGroupMemberViewSet, ImportLanguagesView, LanguageTypeViewSet, LanguageViewSet, \
    NotificationsViewSet, EngagementPresetsViewset, NetworkLocationsViewset, UserContactInfoViewSet, \
    ProductAPIScanConfigurationViewSet, UserProfileView, EndpointMetaImporterView, \
    ConfigurationPermissionViewSet, QuestionnaireQuestionViewSet, QuestionnaireAnswerViewSet, \
    QuestionnaireGeneralSurveyViewSet, QuestionnaireEngagementSurveyViewSet, QuestionnaireAnsweredSurveyViewSet

from dojo.utils import get_system_setting
from dojo.development_environment.urls import urlpatterns as dev_env_urls
from dojo.endpoint.urls import urlpatterns as endpoint_urls
from dojo.engagement.urls import urlpatterns as eng_urls
from dojo.finding.urls import urlpatterns as finding_urls
from dojo.finding_group.urls import urlpatterns as finding_group_urls
from dojo.home.urls import urlpatterns as home_urls
from dojo.metrics.urls import urlpatterns as metrics_urls
from dojo.product.urls import urlpatterns as prod_urls
from dojo.product_type.urls import urlpatterns as pt_urls
from dojo.reports.urls import urlpatterns as reports_urls
from dojo.search.urls import urlpatterns as search_urls
from dojo.test.urls import urlpatterns as test_urls
from dojo.test_type.urls import urlpatterns as test_type_urls
from dojo.user.urls import urlpatterns as user_urls
from dojo.group.urls import urlpatterns as group_urls
from dojo.jira_link.urls import urlpatterns as jira_urls
from dojo.github_issue_link.urls import urlpatterns as github_urls
from dojo.tool_type.urls import urlpatterns as tool_type_urls
from dojo.tool_config.urls import urlpatterns as tool_config_urls
from dojo.tool_product.urls import urlpatterns as tool_product_urls
from dojo.cred.urls import urlpatterns as cred_urls
from dojo.sla_config.urls import urlpatterns as sla_urls
from dojo.system_settings.urls import urlpatterns as system_settings_urls
from dojo.notifications.urls import urlpatterns as notifications_urls
from dojo.object.urls import urlpatterns as object_urls
from dojo.benchmark.urls import urlpatterns as benchmark_urls
from dojo.notes.urls import urlpatterns as notes_urls
from dojo.note_type.urls import urlpatterns as note_type_urls
from dojo.banner.urls import urlpatterns as banner_urls
from dojo.survey.urls import urlpatterns as survey_urls
from dojo.components.urls import urlpatterns as component_urls
from dojo.regulations.urls import urlpatterns as regulations
from dojo.announcement.urls import urlpatterns as announcement_urls
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

import logging
logger = logging.getLogger(__name__)

admin.autodiscover()

# custom handlers
handler500 = 'dojo.views.custom_error_view'
handler400 = 'dojo.views.custom_bad_request_view'

# v2 api written in django-rest-framework
v2_api = DefaultRouter()
v2_api.register(r'technologies', AppAnalysisViewSet)
v2_api.register(r'configuration_permissions', ConfigurationPermissionViewSet)
v2_api.register(r'credentials', CredentialsViewSet)
v2_api.register(r'credential_mappings', CredentialsMappingViewSet)
v2_api.register(r'endpoints', EndPointViewSet)
v2_api.register(r'endpoint_meta_import', EndpointMetaImporterView, basename='endpointmetaimport')
v2_api.register(r'endpoint_status', EndpointStatusViewSet)
v2_api.register(r'engagements', EngagementViewSet)
v2_api.register(r'development_environments', DevelopmentEnvironmentViewSet)
v2_api.register(r'finding_templates', FindingTemplatesViewSet)
v2_api.register(r'findings', FindingViewSet)
v2_api.register(r'jira_configurations', JiraInstanceViewSet)  # backwards compatibility
v2_api.register(r'jira_instances', JiraInstanceViewSet)
v2_api.register(r'jira_finding_mappings', JiraIssuesViewSet)
v2_api.register(r'jira_product_configurations', JiraProjectViewSet)  # backwards compatibility
v2_api.register(r'jira_projects', JiraProjectViewSet)
v2_api.register(r'products', ProductViewSet)
v2_api.register(r'product_types', ProductTypeViewSet)
v2_api.register(r'dojo_groups', DojoGroupViewSet)
v2_api.register(r'dojo_group_members', DojoGroupMemberViewSet)
v2_api.register(r'product_type_members', ProductTypeMemberViewSet)
v2_api.register(r'product_members', ProductMemberViewSet)
v2_api.register(r'product_type_groups', ProductTypeGroupViewSet)
v2_api.register(r'product_groups', ProductGroupViewSet)
v2_api.register(r'roles', RoleViewSet)
v2_api.register(r'global_roles', GlobalRoleViewSet)
v2_api.register(r'sla_configurations', SLAConfigurationViewset)
v2_api.register(r'sonarqube_issues', SonarqubeIssueViewSet)
v2_api.register(r'sonarqube_transitions', SonarqubeIssueTransitionViewSet)
v2_api.register(r'product_api_scan_configurations', ProductAPIScanConfigurationViewSet)
v2_api.register(r'stub_findings', StubFindingsViewSet)
v2_api.register(r'tests', TestsViewSet)
v2_api.register(r'test_types', TestTypesViewSet)
v2_api.register(r'test_imports', TestImportViewSet)
v2_api.register(r'tool_configurations', ToolConfigurationsViewSet)
v2_api.register(r'tool_product_settings', ToolProductSettingsViewSet)
v2_api.register(r'tool_types', ToolTypesViewSet)
v2_api.register(r'users', UsersViewSet)
v2_api.register(r'user_contact_infos', UserContactInfoViewSet)
v2_api.register(r'import-scan', ImportScanView, basename='importscan')
v2_api.register(r'reimport-scan', ReImportScanView, basename='reimportscan')
v2_api.register(r'metadata', DojoMetaViewSet, basename='metadata')
v2_api.register(r'notes', NotesViewSet)
v2_api.register(r'note_type', NoteTypeViewSet)
v2_api.register(r'system_settings', SystemSettingsViewSet)
v2_api.register(r'regulations', RegulationsViewSet)
v2_api.register(r'risk_acceptance', RiskAcceptanceViewSet)
v2_api.register(r'language_types', LanguageTypeViewSet)
v2_api.register(r'languages', LanguageViewSet)
v2_api.register(r'import-languages', ImportLanguagesView, basename='importlanguages')
v2_api.register(r'notifications', NotificationsViewSet, basename='notifications')
v2_api.register(r'engagement_presets', EngagementPresetsViewset)
v2_api.register(r'network_locations', NetworkLocationsViewset)
v2_api.register(r'questionnaire_answers', QuestionnaireAnswerViewSet)
v2_api.register(r'questionnaire_answered_questionnaires', QuestionnaireAnsweredSurveyViewSet)
v2_api.register(r'questionnaire_engagement_questionnaires', QuestionnaireEngagementSurveyViewSet)
v2_api.register(r'questionnaire_general_questionnaires', QuestionnaireGeneralSurveyViewSet)
v2_api.register(r'questionnaire_questions', QuestionnaireQuestionViewSet)
ur = []
ur += dev_env_urls
ur += endpoint_urls
ur += eng_urls
ur += finding_urls
ur += finding_group_urls
ur += home_urls
ur += metrics_urls
ur += prod_urls
ur += pt_urls
ur += reports_urls
ur += search_urls
ur += test_type_urls
ur += test_urls
ur += user_urls
ur += group_urls
ur += jira_urls
ur += github_urls
ur += tool_type_urls
ur += tool_config_urls
ur += tool_product_urls
ur += cred_urls
ur += sla_urls
ur += system_settings_urls
ur += notifications_urls
ur += object_urls
ur += benchmark_urls
ur += notes_urls
ur += note_type_urls
ur += banner_urls
ur += component_urls
ur += regulations
ur += announcement_urls

api_v2_urls = [
    #  Django Rest Framework API v2
    re_path(r'^%sapi/v2/' % get_system_setting('url_prefix'), include(v2_api.urls)),
    re_path(r'^%sapi/v2/user_profile/' % get_system_setting('url_prefix'), UserProfileView.as_view(), name='user_profile'),
]

if hasattr(settings, 'API_TOKENS_ENABLED'):
    if settings.API_TOKENS_ENABLED:
        api_v2_urls += [
            re_path(
                f"^{get_system_setting('url_prefix')}api/v2/api-token-auth/",
                tokenviews.obtain_auth_token,
                name='api-token-auth',
            )
        ]

schema_view = get_schema_view(
    openapi.Info(
        title="Defect Dojo API",
        default_version='v2',
        description="To use the API you need be authorized.",
    ),
    # if public=False, includes only endpoints the current user has access to
    public=True,
    # The API of a OpenSource project should be public accessible
    permission_classes=[permissions.AllowAny],
    # url pattersns specific to the API
    patterns=api_v2_urls,
)

urlpatterns = [
    # action history
    re_path(r'^%shistory/(?P<cid>\d+)/(?P<oid>\d+)$' % get_system_setting('url_prefix'), views.action_history, name='action_history'),
    re_path(r'^%s' % get_system_setting('url_prefix'), include(ur)),

    # drf-yasg = OpenAPI2
    re_path(r'^%sapi/v2/doc/' % get_system_setting('url_prefix'), schema_view.with_ui('swagger', cache_timeout=0), name='api_v2_schema'),

    # drf-spectacular = OpenAPI3
    re_path(r'^%sapi/v2/oa3/schema/' % get_system_setting('url_prefix'), SpectacularAPIView.as_view(), name='schema_oa3'),
    re_path(r'^%sapi/v2/oa3/swagger-ui/' % get_system_setting('url_prefix'), SpectacularSwaggerView.as_view(url=get_system_setting('url_prefix') + '/api/v2/oa3/schema/?format=json'), name='swagger-ui_oa3'),

    re_path(r'^robots.txt', lambda x: HttpResponse("User-Agent: *\nDisallow: /", content_type="text/plain"), name="robots_file"),
    re_path(r'^manage_files/(?P<oid>\d+)/(?P<obj_type>\w+)$', views.manage_files, name='manage_files'),
    re_path(r'^access_file/(?P<fid>\d+)/(?P<oid>\d+)/(?P<obj_type>\w+)$', views.access_file, name='access_file'),
    re_path(r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'), views.protected_serve, {'document_root': settings.MEDIA_ROOT})
]

urlpatterns += api_v2_urls
urlpatterns += survey_urls

if hasattr(settings, 'DJANGO_METRICS_ENABLED'):
    if settings.DJANGO_METRICS_ENABLED:
        urlpatterns += [re_path(r'^%sdjango_metrics/' % get_system_setting('url_prefix'), include('django_prometheus.urls'))]

if hasattr(settings, 'SAML2_ENABLED'):
    if settings.SAML2_ENABLED:
        # django saml2
        urlpatterns += [re_path(r'^saml2/', include('djangosaml2.urls'))]

if hasattr(settings, 'DJANGO_ADMIN_ENABLED'):
    if settings.DJANGO_ADMIN_ENABLED:
        #  django admin
        urlpatterns += [re_path(r'^%sadmin/' % get_system_setting('url_prefix'), admin.site.urls)]

# sometimes urlpatterns needed be added from local_settings.py to avoid having to modify core defect dojo files
if hasattr(settings, 'EXTRA_URL_PATTERNS'):
    urlpatterns += settings.EXTRA_URL_PATTERNS
