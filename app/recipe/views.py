"""
Views for the Recipe APIs
"""

from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """ View for manage recipe APIs """
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Retrieve recipe for authenticated users """
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """ Return the serializer class for the 'list' request """
        # When user request for list of recipes, 'action' is set to 'list'
        # and we end up in this section of the code for 'get_serializer_class'
        # otherwise we know there is a update/create/delete action which contains
        # 'description', which will require the RecipeDetailSerializer, and that will
        # not have a 'list' action and will be handles by the code in the body
        # of the class.
        if self.action == 'list':
            # avoid the ending () to get a reference to the class
            # not the object.
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """ Create a new recipe. """
        serializer.save(user=self.request.user)


class TagViewSet(mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """ Manage Tags in the Database """
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Filter queryset to authenticated user """
        return self.queryset.filter(user=self.request.user).order_by('-name')


class IngredientViewSet(mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """ Manage ingredients in the database. """
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Filter queryset to authenticated user. """
        return self.queryset.filter(user=self.request.user).order_by('-name')


