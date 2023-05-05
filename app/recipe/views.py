"""
Views for the Recipe APIs
"""

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
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

    def _params_to_ints(self, qs):
        """ Convert a list if strings to integers """
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """ Retrieve recipe for authenticated users """
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            # These __ filed names are how Django 'related fields"
            # are referenced in the database.
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        # Since multiple values of tags or ingredients, may
        # be in the queryset, we would like to ger
        # a 'unique' list, therefore we call 'distinct()'
        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()

    def get_serializer_class(self):
        """ Return the serializer class for the 'list' request """
        # When user request for list of recipes, 'action' is set to 'list'
        # and we end up in this section of the code for 'get_serializer_class'
        # otherwise we know there is a update/create/delete action which contains
        # 'description', which will require the RecipeDetailSerializer, and that will
        # not have a 'list' action and will be handles by the code in the body
        # of the class.
        # Note: 'List' action is defined in ModelViewSet.
        if self.action == 'list':
            # avoid the ending () to get a reference to the class
            # not the object.
            return serializers.RecipeSerializer
        # Note: 'upload_image' is not defined action in the
        # ModelViewSet. We need to define it ourselves, in this class
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """ Create a new recipe. """
        serializer.save(user=self.request.user)

    # In this method/acton, we are only accepting 'POST'
    # detail=True ==> this action applies only to the deail
    #                 portion of our ModelViewSet. 'detail'
    #                 refers to a recipe with a specific id
    # The custom url path = 'upload-image'
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """ Upload an image to recipe. """
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,  # To delete an ingredient
                            mixins.UpdateModelMixin,   # To update an ingredient
                            mixins.ListModelMixin,     # To list ingredients
                            viewsets.GenericViewSet):
    """ Base viewset for recipe attributes """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Filter queryset to authenticated user """
        return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(BaseRecipeAttrViewSet):
    """ Manage Tags in the Database """
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """ Manage ingredients in the database. """
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()



