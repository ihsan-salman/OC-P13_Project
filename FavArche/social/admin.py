'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.contrib import admin
from django.core.paginator import Paginator
from django.core.cache import cache

from .models import Comment, Like, ChatRoom, ChatMessage


admin.site.register(Comment)
admin.site.register(Like)


class ChatRoomAdmin(admin.ModelAdmin):
    ''' chat room admin class '''
    list_display = ['id', 'title']
    search_fields = ['id', 'title']
    list_display = ['id']

    class Meta:
        ''' meta class '''
        model = ChatRoom


admin.site.register(ChatRoom, ChatRoomAdmin)


class CachingPaginator(Paginator):
    ''' caching paginator to display correctly '''
    def _get_count(self):

        if not hasattr(self, '_count'):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(
                        hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count()
                    cache.set(key, self._count, 3600)

            except:
                self._count = len(self.object_list)
        return self._count

    count = property(_get_count)


class RoomChatMessageAdmin(admin.ModelAdmin):
    ''' room chat message admin class '''
    list_filter = ['room', 'user', 'timestamp']
    list_display = ['room', 'user', 'timestamp', 'content']
    search_fields = ['room__title', 'user__username', 'content']
    readonly_fields = ['id', 'user', 'room', 'timestamp']

    show_full_result_count = False
    paginator = CachingPaginator

    class Meta:
        ''' class meta '''
        model = ChatMessage


admin.site.register(ChatMessage, RoomChatMessageAdmin)
