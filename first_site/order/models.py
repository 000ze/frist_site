from django.db import models

# Create your models here.

# 订单管理系统, 书  作者 出版社


# 商家
class Merchant(models.Model):
    id = models.AutoField(primary_key=True)  # 自增的ID主键
    # 创建一个varchar(64)的唯一的不为空的字段
    name = models.CharField(max_length=64, null=False, unique=True)
    addr = models.CharField(max_length=128)

    def __str__(self):
        return "<Merchant Object: {}>".format(self.name)


# 商品
class Product(models.Model):
    id = models.AutoField(primary_key=True)  # 自增的ID主键
    # 创建一个varchar(64)的唯一的不为空的字段
    title = models.CharField(max_length=64, null=False, unique=True)
    # 和商家关联的外键字段
    merchant = models.ForeignKey(to="Merchant")

    def __str__(self):
        return "<Product Object: {}>".format(self.title)


# 用户
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16, null=False, unique=True)
    # 告诉ORM 我这张表和产品表是多对多的关联关系,ORM自动帮我生成了第三张表
    product = models.ManyToManyField(to="Product")

    def __str__(self):
        return "<User Object: {}>".format(self.name)