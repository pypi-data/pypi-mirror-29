from wordpress_xmlrpc import Client, WordPressPost, WordPressComment
from wordpress_xmlrpc.methods.posts import NewPost, DeletePost, GetPost, EditPost
from wordpress_xmlrpc.methods.comments import NewComment

from ScopusWp.wordpress.config import WordpressConfig
from ScopusWp.wordpress.views import PublicationPostView, PublicationCommentView

import datetime


class WordpressPublicationController:

    def __init__(self):
        self.config = WordpressConfig.get_instance()

        self.url = self.config['WORDPRESS']['url']
        self.username = self.config['WORDPRESS']['username']
        self.password = self.config['WORDPRESS']['password']

        # The client for the wordpress xmlrpc communication
        self.client = Client(
            self.url,
            self.username,
            self.password
        )

    def post(self, general_publication):
        post_reference_dict = self.post_publication(general_publication)
        comment_reference_dict_list = self.post_comments(
            post_reference_dict['post'],
            general_publication.citations
        )
        post_reference_dict['comments'] = comment_reference_dict_list
        return post_reference_dict

    def post_publication(self, general_publication):
        view = PublicationPostView(general_publication)

        post = WordPressPost()
        post.title = view.title()
        post.excerpt = view.excerpt()
        post.slug = view.slug()
        post.content = view.content()
        post.date = view.date()
        post.terms_names = {
            'category': view.categories(),
            'post_tag': view.tags()
        }
        post.post_status = 'publish'
        post.comment_status = 'closed'

        post_id = self.client.call(NewPost(post))

        return {
            'publication': general_publication.id,
            'post': post_id,
            'published': datetime.datetime.now(),
            'comments': []
        }

    def post_comments(self, post_id, general_publication_list):
        comment_reference_dict_list = []
        self.enable_comments(post_id)
        for general_publication in general_publication_list:
            comment_reference_dict = self.post_comment(post_id, general_publication)
            comment_reference_dict_list.append(comment_reference_dict)
        self.disable_comments(post_id)
        return comment_reference_dict_list

    def post_comment(self, post_id, general_publication):
        view = PublicationCommentView(general_publication)

        comment = WordPressComment()
        comment.content = view.content()
        comment.date_created = view.date()

        comment_id = self.client.call(NewComment(post_id, comment))
        return {
            'publication': general_publication.id,
            'post': post_id,
            'comment': comment_id,
            'published': datetime.datetime.now()
        }

    def delete_post(self, post_id):
        self.client.call(DeletePost(post_id))

    def enable_comments(self, post_id):
        post = self.client.call(GetPost(post_id))
        post.comment_status = 'open'
        self.client.call(EditPost(post_id, post))

    def disable_comments(self, post_id):
        post = self.client.call(GetPost(post_id))
        post.comment_status = 'closed'
        self.client.call(EditPost(post_id, post))
