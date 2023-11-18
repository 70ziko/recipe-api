from rest_framework import serializers

from .models import Recipe, RecipeCategory, RecipeLike


class RecipeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCategory
        fields = ('name',)


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    category = RecipeCategorySerializer()
    total_number_of_likes = serializers.SerializerMethodField()
    total_number_of_bookmarks = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'category', 'category_name', 'picture', 'title', 'desc',
                  'cook_time', 'ingredients', 'procedure', 'author', 'username',
                  'total_number_of_likes', 'total_number_of_bookmarks')

    def get_username(self, obj):
        return obj.author.username

    def get_category_name(self, obj):
        return obj.category.name

    def get_total_number_of_likes(self, obj):
        return obj.get_total_number_of_likes()

    def get_total_number_of_bookmarks(self, obj):
        return obj.get_total_number_of_bookmarks()

    # def to_representation(self, obj):
    #     """Move fields from profile to user representation."""
    #     representation = super().to_representation(obj)
    #     category_representation = representation.pop('category')
    #     for key in category_representation:
    #         representation[key] = category_representation[key]
    #     return representation

    def to_internal_value(self, data):
        """Move fields related to profile to their own profile dictionary."""
        data = data.dict()
        category_internal = {}
        for key in RecipeCategorySerializer.Meta.fields:
            if key in data:
                category_internal[key] = data.pop(key)
        data["category"] = category_internal
        internal = super().to_internal_value(data)
        internal['category'] = category_internal
        return internal

    def create(self, validated_data):
        category = validated_data.pop('category')
        category_instance, created = RecipeCategory.objects.get_or_create(
            **category)
        recipe_instance = Recipe.objects.create(
            **validated_data, category=category_instance)
        return recipe_instance

    def update(self, instance, validated_data):
        if 'category' in validated_data:
            nested_serializer = self.fields['category']
            nested_instance = instance.category
            nested_data = validated_data.pop('category')

            nested_serializer.update(nested_instance, nested_data)

        return super(RecipeSerializer, self).update(instance, validated_data)


class RecipeLikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RecipeLike
        fields = ('id', 'user', 'recipe')
