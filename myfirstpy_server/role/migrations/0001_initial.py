# Generated by Django 4.2.16 on 2024-09-25 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("user", "0002_rename_avater_sysuser_avatar"),
    ]

    operations = [
        migrations.CreateModel(
            name="SysRole",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "name",
                    models.CharField(max_length=30, null=True, verbose_name="角色名称"),
                ),
                (
                    "code",
                    models.CharField(max_length=100, null=True, verbose_name="角色权限字符串"),
                ),
                ("create_time", models.DateField(null=True, verbose_name="创建时间")),
                ("update_time", models.DateField(null=True, verbose_name="更新时间")),
                (
                    "remark",
                    models.CharField(max_length=500, null=True, verbose_name="备注"),
                ),
            ],
            options={
                "db_table": "sys_role",
            },
        ),
        migrations.CreateModel(
            name="SysUserRole",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "role",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="role.sysrole"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="user.sysuser"
                    ),
                ),
            ],
            options={
                "db_table": "sys_user_role",
            },
        ),
    ]
