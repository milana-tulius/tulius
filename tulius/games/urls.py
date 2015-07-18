from django.conf.urls import patterns, url
from .views import *
from .game_edit_catalog import *
from .game_edit_views import *
from .requests_view import make_game_request, cancel_game_request, role_assign_user, role_clear_user

urlpatterns = patterns ('',
    # game list and details
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^announced/$', AnnouncedGames.as_view(), name='announced_games'),
    url(r'^accepting/$', RequestAcceptingGames.as_view(), name='request_accepting_games'),
    url(r'^awaiting_start/$', AwaitingStartGames.as_view(), name='awaiting_start_games'),
    url(r'^current/$', CurrentGames.as_view(), name='current_games'),
    url(r'^completed/$', CompletedOpenedGames.as_view(), name='completed_opened_games'),
    url(r'^add_game/(?P<pk>\d+)/$', CreateGame.as_view(), name='add_game'),
    url(r'^game/(?P<pk>\d+)/$', GameView.as_view(), name='game'),
    url(r'^delete_game/(?P<pk>\d+)/$', DeleteGame.as_view(), name='delete_game'),
    url(r'^change_story/(?P<pk>\d+)/$', ChangeGameStoryView.as_view(), name='change_game_story'),
    url(r'^view_role/(?P<pk>\d+)/$', GameRoleView.as_view(), name='view_role'),
    url(r'^edit_game/(?P<game_id>\d+)/main/$', GameAdminMain.as_view(), name=EDIT_GAME_PAGES_MAIN),
    url(r'^edit_game/(?P<game_id>\d+)/texts/$', GameAdminTexts.as_view(), name=EDIT_GAME_PAGES_TEXTS),
    url(r'^edit_game/(?P<game_id>\d+)/users/$', GameAdminUsers.as_view(), name=EDIT_GAME_PAGES_USERS),
    url(r'^edit_game/(?P<game_id>\d+)/graphics/$', GameAdminGraphics.as_view(), name=EDIT_GAME_PAGES_GRAPHICS),
    url(r'^edit_game/(?P<game_id>\d+)/roles/$', GameEditRoles.as_view(), name=EDIT_GAME_PAGES_ROLES),
    url(r'^edit_game/(?P<pk>\d+)/illustrations/$', GameEditIllustrationsView.as_view(), name=EDIT_GAME_PAGES_ILLUSTRATIONS),
    url(r'^edit_game/(?P<pk>\d+)/materials/$', GameEditMaterialsView.as_view(), name=EDIT_GAME_PAGES_MATERIALS),
    url(r'^edit_game/(?P<pk>\d+)/request_form/$', EditRequestView.as_view(), name=EDIT_GAME_PAGES_REQUEST_FORM),
    url(r'^edit_game/(?P<pk>\d+)/requests/$', EditRequestsView.as_view(), name=EDIT_GAME_PAGES_REQUESTS),
    url(r'^edit_game/(?P<pk>\d+)/winners/$', EditWinnersView.as_view(), name=EDIT_GAME_PAGES_WINNERS),
    url(r'^edit_game/(?P<pk>\d+)/forum/$', GameForumView.as_view(), name=EDIT_GAME_PAGES_FORUM),
    url(r'^edit_game/(?P<game_id>\d+)/players/$', game_edit_players, name='game_edit_players'),
        
    url(r'^edit_game/(?P<pk>\d+)/add_role/$', AddRoleView.as_view(), name='add_role'),
    url(r'^edit_game/(?P<pk>\d+)/add_material/$', AddMaterialView.as_view(), name='add_material'),
    url(r'^role/(?P<pk>\d+)/$', GameEditRoleView.as_view(), name='role'),
    url(r'^role/(?P<pk>\d+)/text/$', GameRoleTextView.as_view(), name='role_text'),
    url(r'^role/(?P<pk>\d+)/assign/$', EditRoleAssignView.as_view(), name='role_assign'),
    url(r'^edit_illustration/(?P<pk>\d+)/$', EditIllustrationView.as_view(), name='edit_illustration'),
    url(r'^edit_illustration/(?P<pk>\d+)/delete/$', DeleteIllustration.as_view(), name='illustration_delete'),
    url(r'^edit_material/(?P<pk>\d+)/$', EditMaterialView.as_view(), name='edit_material'),
    url(r'^edit_material/(?P<pk>\d+)/delete/$', DeleteMaterial.as_view(), name='material_delete'),
    url(r'^material/(?P<pk>\d+)/$', MaterialView.as_view(), name='material'),
    
    url(r'^game_request/(?P<game_id>\d+)/$', make_game_request, name='game_request'),
    url(r'^game_invite/(?P<game_id>\d+)/$', invite_player, name='game_invite'),
    url(r'^cancel_request/(?P<game_id>\d+)/$', cancel_game_request, name='cancel_game_request'),
    url(r'^role/(?P<role_id>\d+)/assign(?P<user_id>\d+)/$', role_assign_user, name='role_assign_user'),
    url(r'^role/(?P<role_id>\d+)/assign(?P<user_id>\d+)/roles/$', role_assign_user, {'backtoroles': True}, name='role_assign_user_roles'),
    url(r'^role/(?P<role_id>\d+)/clearuser/$', role_clear_user, name='role_clear_user'),
)
