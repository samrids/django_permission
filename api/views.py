from snippets.models import Snippets
from api.serializers import SnippetSerializer, AvatarSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from rest_framework.decorators import api_view , schema, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser 




class SnippetList(APIView):
    permission_classes = (IsAuthenticated,)
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Snippets.objects.all().order_by('-id')
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnippetDetail(APIView):
    permission_classes = (IsAuthenticated,)    
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Snippets.objects.get(pk=pk)
        except Snippets.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippets = self.get_object(pk)
        serializer = SnippetSerializer(snippets)
        return Response(serializer.data)
        
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def patch(self, request, pk, format=None):       
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data, partial=True)

        chkfields = list()
        fieldslist = list(serializer.fields)
        for k, v in request.data.items():
            if k not in fieldslist:
                chkfields.append(k)        

        if ((serializer.is_valid()) and (len(chkfields) == 0)):
            serializer.save()
            return Response(serializer.data)

        if len(chkfields) > 0:
            err_str = {"detail: Field(s) incorrect !": chkfields}
            return Response(err_str, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        


class AvatarUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get_object(self, pk):
        try:
            return Snippets.objects.get(pk=pk)
        except Snippets.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = AvatarSerializer(snippet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)