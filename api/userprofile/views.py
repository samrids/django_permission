from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from api.userprofile.serializers import RegistrationSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

# Verification email
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission, SAFE_METHODS

from rest_framework.permissions import DjangoObjectPermissions

from django.http import Http404

from userprofile.models import Profile
from rest_framework import permissions

class RegistrationAPIView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()        
            profile = Profile(user=user)
            profile.save()

            # USER ACTIVATION
            current_site = '127.0.0.1:8000'
            mail_subject = 'Please activate your account'
            message = render_to_string('api/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = serializer.data['email']
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            #send_email.send()                          

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def Activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('/accounts/login/') #TODO
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('/accounts/login/') #TODO 


class CustomUserPermission(permissions.BasePermission):

    def is_group_allow(self, theperm):
        # Return True if user in Groups
        for group in theperm:
            if group in ['supervisor', 'manager']:
                return True
        
        return False

    def has_permission(self, request, view):
        
        custom_perms = request.user.groups.values_list('name',flat=True) 
        perm_groups = list(custom_perms)  
        
        is_GroupAllow = self.is_group_allow(perm_groups)     #Check with group (Has 3 Groups [manager, supervisor, staff], see an images)
        if not is_GroupAllow:
            return request.user == User.objects.get(pk=view.kwargs['pk'])

        #return request.user.has_perm('userprofile.change_profile') #Check with has_perm('foo.change_bar')
class UpdateFirstLast_Name(APIView):    
    
    """
    Update first_name, last_name
    """
    permission_classes = (CustomUserPermission,)

    def get_object(self, pk):
        try:
            return User._default_manager.get(pk=pk)
        except User.DoesNotExist:
            raise Http404    
    
    def patch(self, request, pk, format=None):       
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)

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