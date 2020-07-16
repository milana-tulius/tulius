from django.conf.urls import url
from django.views import generic

from .core import CommentsCore
from .views import CommentRedirrect


class Index(generic.TemplateView):
    template_name = 'base_vue.html'


class CommentsPlugin(CommentsCore):
    comment_template = 'forum/snippets/post.haml'

    def get_paged_url(self, comment):
        return "%s?page=%s#%s" % (
            self.reverse('thread', comment.parent_id),
            comment.page, comment.id)

    def get_page_num(self, comment):
        num = self.models.Comment.objects.filter(
            parent=comment.parent, id__lt=comment.id, deleted=False).count()
        return (num / self.COMMENTS_ON_PAGE) + 1

    def init_core(self):
        super(CommentsPlugin, self).init_core()
        self.urlizer['comment_paged'] = self.get_paged_url
        self.urlizer['Comment_get_paged_url'] = self.get_paged_url
        self.core['Comment_get_page_num'] = self.get_page_num

    def get_urls(self):
        return [
            url(
                r'^edit_comment/(?P<comment_id>\d+)/$',
                Index.as_view(),
                name='edit_comment'),
            url(
                r'^comment/(?P<comment_id>\d+)/$',
                CommentRedirrect.as_view(plugin=self),
                name='comment'),
        ]
