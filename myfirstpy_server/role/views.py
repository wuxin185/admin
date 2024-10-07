from datetime import datetime

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View

from menu.models import SysRoleMenu
from role.models import SysRole, SysRoleSerializer, SysUserRole


# Create your views here.
# 查询所有角色信息
class ListAllView(View):
    def get(self, request):
        obj_roleList = SysRole.objects.all().values()  # 转成字典
        roleList = list(obj_roleList)  # 把外层的容器转为List
        return JsonResponse({'code': 200, 'roleList': roleList})


# 角色信息查询
class SearchView(View):
    def post(self, request):
        data = {
            'pageNum': request.GET.get('pageNum'),
            'pageSize': request.GET.get('pageSize'),
            'query': request.GET.get('query'),
        }
        pageNum = data['pageNum']  # 当前页
        pageSize = data['pageSize']  # 每页大小
        query = data['query']  # 查询参数
        print(pageSize, pageNum)
        roleListPage = Paginator(SysRole.objects.filter(name__icontains=query),
                                 pageSize).page(pageNum)
        obj_roles = roleListPage.object_list.values()  # 转成字典
        roles = list(obj_roles)  # 把外层的容器转为List
        total = SysRole.objects.filter(name__icontains=query).count()
        return JsonResponse({'code': 200, 'roleList': roles, 'total': total})


class SaveView(View):
    def post(self, request):
        data = {
            'id': request.POST.get('id'),
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'code': request.POST.get('code'),
            'remark': request.POST.get('remark'),
            'create_time': request.POST.get('create_time'),
            'update_time': request.POST.get('update_time'),
        }
        if data['id'] == -1:  # 添加
            obj_sysRole = SysRole(name=data['name'], code=data['code'],
                                  remark=data['remark'])
            obj_sysRole.create_time = datetime.now().date()
            obj_sysRole.save()
        else:  # 修改
            obj_sysRole = SysRole(id=data['id'], name=data['name'],
                                  code=data['code'],
                                  remark=data['remark'],
                                  create_time=data['create_time'],
                                  update_time=data['update_time'])
            obj_sysRole.update_time = datetime.now().date()
            obj_sysRole.save()
        return JsonResponse({'code': 200})


# 角色基本操作
class ActionView(View):
    def get(self, request):
        """
        根据id获取角色信息
        :param request:
        :return:
        """
        id = request.GET.get("id")
        role_object = SysRole.objects.get(id=id)
        return JsonResponse({'code': 200, 'role': SysRoleSerializer(role_object).data})

    def delete(self, request):
        """
        删除操作
        :param request:
        :return:
        """

        idList = request.GET.get('ids')
        idList = idList.split(',')
        print(idList)

        SysUserRole.objects.filter(role_id__in=idList).delete()
        SysRoleMenu.objects.filter(role_id__in=idList).delete()
        SysRole.objects.filter(id__in=idList).delete()
        return JsonResponse({'code': 200})


# 根据角色查询菜单权限
class MenusView(View):
    def get(self, request):
        id = request.GET.get("id")
        menuList = SysRoleMenu.objects.filter(role_id=id).values("menu_id")
        menuIdList = [m['menu_id'] for m in menuList]
        print("menuIdList=", menuIdList)

        return JsonResponse({'code': 200, 'menuIdList': menuIdList})


# 角色权限授权
class GrantMenu(View):
    def post(self, request):
        data = {
            'id': request.GET.get('id'),
        }
        role_id = data['id']
        menuIdList = request.GET.getlist('menuIds[]')  # 获取 menuIds[]

        # 转换为整数（如果需要）
        menuIdList = list(map(int, menuIdList))

        print(role_id, menuIdList)
        SysRoleMenu.objects.filter(role_id=role_id).delete()  # 删除角色菜单关联表中的指定角色数据
        for menuId in menuIdList:
            roleMenu = SysRoleMenu(role_id=role_id, menu_id=menuId)
            roleMenu.save()
        return JsonResponse({'code': 200})
