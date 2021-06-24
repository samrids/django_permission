from django.shortcuts import render

def testuserperms(request):
    #แบบที่ 1
    context={
        'can_add'    : request.user.has_perm('app.add_task'),
        'can_change' : request.user.has_perm('app.change_task'),
        'can_delete' : request.user.has_perm('app.delete_task'),
        'can_view'   : request.user.has_perm('app.view_task')
    }

    # แบบที่ 2
    # context={
    #     'can_add'    : 'app.add_task'    in request.user.get_group_permissions(), 
    #     'can_change' : 'app.change_task' in request.user.get_group_permissions(), 
    #     'can_delete' : 'app.delete_task' in request.user.get_group_permissions(), 
    #     'can_view'   : 'app.view_task'   in request.user.get_group_permissions() 
    # }

    return render(request,'home.html', context=context)