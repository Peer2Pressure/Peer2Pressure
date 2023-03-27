

# Third-party libraries
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from varname import nameof

# Local libraries
from .. models import Author
# from ..utils import validate_followers_url_path

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="author" , max_length=10, read_only=True)
    host = serializers.URLField(required=False)
    id = serializers.URLField(required=True)
    url = serializers.URLField(required=False)
    displayName = serializers.CharField(source="name", max_length=100, required=False)
    # username = serializers.CharField(max_length=300, required=False)
    github = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    profileImage = serializers.URLField(source="avatar", required=False, allow_null=True, allow_blank=True)

    # TODO: Set required attribute true for certain methods
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.context['request'].method in ['POST', 'PUT']:
    #         self.fields['my_field'].required = True
    
    class Meta:
        model = Author
        fields = ["type", "id", "url", "host", "displayName", "github", "profileImage"]
        # extra_kwargs = {'image': {'required': False, 'allow_null': True}}

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        # instance.username = validated_data.get("username", instance.username)
        instance.username = validated_data.get("github", instance.github)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.save()
        return instance
    
    # def create(self, validated_data):
    #     return Author.objects.create(
    #         id=validated_data['id'],
    #         host=validated_data['host'],
    #         username='',
    #         name=validated_data['displayName'],
    #         url=validated_data['url'],
    #         email='',
    #         password='',
    #         avatar=validated_data.get('profileImage')
    # )

    def create_author(self, username, name, email, password, host = None, id = None, user=None):

        defaults = {
            nameof(Author.username): username,
            nameof(Author.name): name,
            nameof(Author.email): email,
            nameof(Author.password): password
        }

        if id is not None:
            try:
                author_obj = self.get_author_by_id(id)
            except ValueError:
                defaults[Author.id] = id

        if host is not None:
            defaults[nameof(Author.host)] = host

        if user is not None:
            defaults[nameof(Author.user)] = user

        # print("Defautls: ", defaults)

        author_obj = Author.objects.create(**defaults)

        return author_obj.id
    
    def get_author_id_by_username(self, username):
        try:
            author_obj = Author.objects.get(username=username)
        except Author.DoesNotExist:
            raise ValueError("Author does not exist")

        return author_obj.id

    def get_author_by_id(self, author_id):
        try:
            author_obj = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            raise ValidationError("Author does not exist")
        
        return author_obj
    
    def author_exists(self, author_id):
        try:
            author = self.get_author_by_id(author_id)
        except ValidationError:
            return False
        return True

class AllAuthorSerializer(serializers.Serializer):
    type = serializers.CharField(default="authors" , max_length=10, read_only=True, required=False)
    page = serializers.IntegerField(allow_null=True, required=False)
    size = serializers.IntegerField(allow_null=True, required=False)
    # items = serializers.ListField()
    items = AuthorSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['page'] is None:
            data.pop('page')
        if data['size'] is None:
            data.pop('size')
        return data
