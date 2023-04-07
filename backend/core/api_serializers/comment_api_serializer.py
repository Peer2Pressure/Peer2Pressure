from rest_framework import serializers

from .. import utils
from ..models import *
from ..serializers.postserializer import PostSerializer
from ..serializers.commentserializer import CommentSerializer
from ..api_serializers.author_api_serializer import AuthorAPISerializer

# Serializers
post_serializer = PostSerializer()
comment_serializer = CommentSerializer()

# API serializer
author_api_serializer = AuthorAPISerializer()

class CommentAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("comment")

    def get_comment_data(self, comment):
        author_data = author_api_serializer.get_author_data(comment.author)

        comment_data = {
            "type": "comment",
            "author": author_data,
            "comment": comment.comment,
            # TODO: Might have to add contentT_type to model
            "contentType": "",      
            "id": comment.url,
            "published": comment.created_at,
            }
        
        return comment_data
    
    def get_single_comment(self, author_id, post_id, comment_id):
        author_data = {}
        try:
            comment = comment_serializer.get_comment_by_id(comment_id)
            comment_data = self.get_comment_data(comment)
        except ValueError:
            return None
        
        return comment_data
    
    def add_new_comment(self, author_id, post_id, request_data):
        """
        Add new comment to the post
        """
        if "comment" in list(request_data.keys()):
            if request_data["comment"] != "":
                comment_id = comment_serializer.create_comment(author_id, post_id, request_data["comment"])
                return self.get_single_comment(author_id, post_id, comment_id)
        
        return None


    def get_post_comments(self, author_id, post_id, page=None, size=None):
        post = None
        try:
            post = post_serializer.get_author_post(author_id, post_id)
        except ValueError:
            return None
        
        comments = post.comment.all()
        
        result_dict = {}
        result_dict["type"] = "comments"
        result_dict["post"] = post.url
        result_dict["id"] = f"{post.url}/comments"

        comments_list = []

        for comment in comments:
            curr_comment_data = self.get_comment_data(comment)
            comments_list.append(curr_comment_data)
 

        if page and size:
            paginated_comments = utils.paginate_list(comments_list, page, size)
            
            result_dict["page"] = page
            result_dict["size"] = size
            result_dict["comments"] = paginated_comments
        else:
            result_dict["comments"] = comments_list

        return result_dict