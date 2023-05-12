from django.urls import path

from api.views import (
    InvateList,
    FriendList,
    InvateCreate,
    InvateDelete,
    InvateAccept,
)


urlpatterns = [
    path('friends/',
         FriendList.as_view(),
         name='friends',
         ),
    path('invate/send/<int:user_id>/',
         InvateCreate.as_view(),
         name='send_invate',
         ),
    path('invate/<int:id_invate>/accept/',
         InvateAccept.as_view(),
         name='accept_invate',
         ),
    path('invate/<int:pk>/delete/',
         InvateDelete.as_view(),
         name='delete_invate',
         ),
    path('invate/show/',
         InvateList.as_view(),
         name='list_invate',
         ),
    path('user/<int:pk>/status_relationship/',
         FriendList.as_view(),
         name='relationship',
         ),
]
