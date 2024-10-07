import uuid
from datetime import datetime

from django.http import JsonResponse
from django.views import View

from menu.models import SysMenu, SysMenuSerializer, SysRoleMenu


# Create your views here.
class TreeListView(View):
    # 构造菜单树
    def buildTreeMenu(self, sysMenuList):
        resultMenuList: list[SysMenu] = list()
        for menu in sysMenuList:
            # 寻找子节点
            for e in sysMenuList:
                if e.parent_id == menu.id:
                    if not hasattr(menu, "children"):
                        menu.children = list()
                    menu.children.append(e)
            # 判断父节点，添加到集合
            if menu.parent_id == 0:
                resultMenuList.append(menu)
        return resultMenuList

    def get(self, request):
        menuQuerySet = SysMenu.objects.order_by("order_num")
        # 构造菜单树
        sysMenuList: list[SysMenu] = self.buildTreeMenu(menuQuerySet)
        serializerMenuList: list[SysMenuSerializer] = list()
        for sysMenu in sysMenuList:
            serializerMenuList.append(SysMenuSerializer(sysMenu).data)
        return JsonResponse({'code': 200, 'treeList': serializerMenuList})


class SaveView(View):
    def post(self, request):
        data = {
            'id': request.GET.get('id'),
            'name': request.GET.get('name'),
            'icon': request.GET.get('icon'),
            'parent_id': request.GET.get('parent_id'),
            'order_num': request.GET.get('order_num'),
            'path': request.GET.get('path'),
            'component': request.GET.get('component'),
            'menu_type': request.GET.get('menu_type'),
            'perms': request.GET.get('perms'),
            'remark': request.GET.get('remark'),
            'create_time': request.GET.get('create_time'),
            'update_time': request.GET.get('update_time'),
        }
        unique_id = str(uuid.uuid4())  # 生成唯一 ID
        print(unique_id)
        if data['id'] == -1:  # 添加
            obj_sysMenu = SysMenu(id=unique_id,  # 手动设置 ID
                                  name=data['name'], icon=data['icon'],
                                  parent_id=data['parent_id'],
                                  order_num=data['order_num'], path=data['path'],
                                  component=data['component'],
                                  menu_type=data['menu_type'], perms=data['perms'],
                                  remark=data['remark'])
            obj_sysMenu.create_time = datetime.now().date()
            obj_sysMenu.save()
        else:  # 修改
            obj_sysMenu = SysMenu(id=data['id'], name=data['name'],
                                  icon=data['icon'],
                                  parent_id=data['parent_id'],
                                  order_num=data['order_num'], path=data['path'],
                                  component=data['component'],
                                  menu_type=data['menu_type'], perms=data['perms'],
                                  remark=data['remark'],
                                  create_time=data['create_time'],
                                  update_time=data['update_time'])
            obj_sysMenu.update_time = datetime.now().date()
            obj_sysMenu.save()
            return JsonResponse({'code': 200})


# 菜单基本操作
class ActionView(View):
    def get(self, request):
        """
        根据id获取权限信息
        :param request:
        :return:
        """
        id = request.GET.get("id")
        menu_object = SysMenu.objects.get(id=id)
        return JsonResponse({'code': 200, 'menu': SysMenuSerializer(menu_object).data})

    def delete(self, request):
        """
        删除操作
        :param request:
        :return:
        """

        id = request.GET.get("id")
        print(id)

        if SysMenu.objects.filter(parent_id=id).count() > 0:
            return JsonResponse({'code': 500, 'msg': '请先删除子菜单！'})
        else:
            SysRoleMenu.objects.filter(menu_id=id).delete()
            SysMenu.objects.get(id=id).delete()
            return JsonResponse({'code': 200})
