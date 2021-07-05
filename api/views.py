from userprofile.models import Profile
from api.serializers import ProfileSerializer, AvatarSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from rest_framework.decorators import api_view , schema, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser 




class ProfileList(APIView):
    permission_classes = (IsAuthenticated,)
    """
    List all profiles, or create a new profile.
    """
    def get(self, request, format=None):
        profiles = Profile.objects.all().order_by('-id')
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileByToken(APIView):
    permission_classes = (IsAuthenticated,)    
    """
    Retrieve, User profile by access token
    """
    def get_object(self, pk):
        try:
            return Profile.objects.get(user_id=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        profile = self.get_object(request.user.id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
        
class ProfileDetail(APIView):
    permission_classes = (IsAuthenticated,)    
    """
    Retrieve, update or delete a profile instance.
    """
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
        
    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def patch(self, request, pk, format=None):       
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)

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
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        


class AvatarUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = AvatarSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)