"""
Serializers for Recipe APIs
"""

from rest_framework import serializers
from core.models import (
    Recipe,
    Tag,
    Ingredient,
)


class IngredientSerializer(serializers.ModelSerializer):
    """ Serializer for ingredients. """

    class Meta:
        model = Ingredient
        # Fields that we wish to use/serialize from this model
        # the 'user' field is pulled form user model.
        fields = ['id', 'name']
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    """ Serializer for tags. """

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer for recipes """
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'time_minutes', 'price', 'link', 'tags',
            'ingredients',
        ]
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        """ handle getting or creating tags as needed """

        # Since we are not in the 'vew', we need to get the user form the 'context'
        # 'context' is passed to the serializer by the view whe using the serializer
        # for the specific view
        auth_user = self.context['request'].user

        # 'get_or_create() is a helper method available for the ModelManager
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        """ Handle getting or creating ingredients as needed """
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, create = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        """ Create a recipe. """
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])

        # once the 'tags' & 'ingredients' are removed from validated_data,
        # create a recipe
        recipe = Recipe.objects.create(**validated_data)

        # Now add the tags & ingredients to recipe
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        """ Update recipe """
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)

        # here we do not user something line 'if tags' since
        # such a check will be true even if the value is None.
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class RecipeDetailSerializer(RecipeSerializer):
    """ Serializer for recipe detail view. """
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']


# This is implemented as a separate class since when images
# are uploaded, they are uploaded apart from other models or data.
class RecipeImageSerializer(serializers.ModelSerializer):
    """ Serializer for uploading images to recipes. """

    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        # add images as a required field.
        extra_kwargs = {'image': {'required': 'True'}}
