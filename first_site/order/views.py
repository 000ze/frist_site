from django.shortcuts import HttpResponse, render, redirect
from order import models


# Create your views here.


# 展示商家列表
def merchant_list(request):
    # 去数据库查出所有的商家,填充到HTML中,给用户返回
    ret = models.Merchant.objects.all().order_by("id")
    return render(request, "merchant_list.html", {"merchant_list": ret})


# 添加新的商家
def add_merchant(request):
    error_msg = ""
    # 如果是POST请求,我就取到用户填写的数据
    if request.method == "POST":
        new_name = request.POST.get("merchant_name", None)
        if new_name:
            # 通过ORM去数据库里新建一条记录
            models.Merchant.objects.create(name=new_name)
            # 引导用户访问出版社列表页,查看是否添加成功  --> 跳转
            return redirect("/merchant_list/")
        else:
            error_msg = "商家名字不能为空!"
    # 用户第一次来,我给他返回一个用来填写的HTML页面
    return render(request, "add_merchant.html", {"error": error_msg})


# 删除商家的函数
def delete_merchant(request):
    # 删除指定的数据
    # 1. 从GET请求的参数里面拿到将要删除的数据的ID值
    del_id = request.GET.get("id", None)  # 字典取值,娶不到默认为None
    # 如果能取到id值
    if del_id:
        # 去数据库删除当前id值的数据
        # 根据id值查找到数据
        del_obj = models.Merchant.objects.get(id=del_id)
        # 删除
        del_obj.delete()
        # 返回删除后的页面,跳转到商家的列表页,查看删除是否成功
        return redirect("/merchant_list/")
    else:
        return HttpResponse("要删除的数据不存在!")


# 编辑商家
def edit_merchant(request):
    # 用户修改完商家的名字,点击提交按钮,给我发来新的商家名字
    if request.method == "POST":
        print(request.POST)
        # 取新商家名字
        edit_id = request.POST.get("id")
        new_name = request.POST.get("merchant_name")
        # 更新商家
        # 根据id取到编辑的是哪个商家
        edit_merchant = models.Merchant.objects.get(id=edit_id)
        edit_merchant.name = new_name
        edit_merchant.save()   # 把修改提交到数据库
        # 跳转商家列表页,查看是否修改成功
        return redirect("/merchant_list/")
        # 从GET请求的URL中取到id参数
    edit_id = request.GET.get("id")
    if edit_id:
        # 获取到当前编辑的商家对象
        merchant_obj = models.Merchant.objects.get(id=edit_id)
        return render(request, "edit_merchant.html", {"merchant": merchant_obj})
    else:
        return HttpResponse("编辑的商家不存在!")


# 展示产品的列表
def product_list(request):
    # 去数据库中查询所有的产品
    all_product = models.Product.objects.all()
    # 在HTML页面完成字符串替换(渲染数据)
    return render(request, "product_list.html", {"all_product": all_product})


# 删除产品
def delete_product(request):
    # 从URL里面获取要删除的产品的id值
    delete_id = request.GET.get("id")  # 从URL里面取数据
    # 去删除数据库中删除指定id的数据
    models.Product.objects.get(id=delete_id).delete()
    # 返回产品产品页面, 查看是否删除成功
    return redirect("/product_list/")


# 添加产品
def add_product(request):
    if request.method == "POST":
        new_title = request.POST.get("product_title")
        new_merchant_id = request.POST.get("merchant")
        # 创建产品对象,自动提交
        models.Product.objects.create(title=new_title, merchant_id=new_merchant_id)



        # 返回到产品列表页
        return redirect("/product_list/")

    # 取到所有的商家
    ret = models.Merchant.objects.all()
    return render(request, "add_product.html", {"merchant_list": ret})


# 编辑产品
def edit_product(request):
    if request.method == "POST":
        # 从提交的数据里面取,产品和该产品关联的商家
        edit_id = request.POST.get("id")
        new_title = request.POST.get("product_title")
        new_merchant_id = request.POST.get("merchant")
        # 更新
        edit_product_obj = models.Product.objects.get(id=edit_id)
        edit_product_obj.title = new_title  # 更新产品名
        edit_product_obj.merchant_id = new_merchant_id  # 更新产品关联的商家
        # 将修改提交到数据库
        edit_product_obj.save()
        # 返回产品列表页面,查看是否编辑成功
        return redirect("/product_list/")

    # 返回一个页面,编辑产品信息
    # 取到编辑的产品的id值
    edit_id = request.GET.get("id")
    # 根据id去数据库中把具体的产品对象拿到
    edit_product_obj = models.Product.objects.get(id=edit_id)
    print(edit_product_obj.id)
    print(edit_product_obj.title)
    print(edit_product_obj.merchant)  # 取到当前产品对象关联的商家对象
    print(edit_product_obj.merchant_id)  # 取到当前产品对象关联的商家的id值

    ret = models.Merchant.objects.all()
    return render(
        request,
        "edit_product.html",
        {"merchant_list": ret, "product_obj": edit_product_obj}
    )


# 用户列表
def user_list(request):

    # 查询所有的用户
    all_user = models.User.objects.all()
    ret = models.Product.objects.all()
    return render(request, "user_list.html", {"user_list": all_user,'products':ret})



# 添加用户
def add_user(request):
    if request.method == "POST":
        print("in post...")
        # 取到提交的数据
        new_user_name = request.POST.get("user_name")
        # post提交的数据是多个值的时候一定会要用getlist,如多选的checkbox和多选的select
        ptoduct = request.POST.getlist("ptoduct")
        # 创建用户
        new_user_obj = models.User.objects.create(name=new_user_name)
        # 把新用户和产品建立对应关系,自动提交
        new_user_obj.product.set(ptoduct)
        # 跳转到用户列表页面,查看是否添加成功!
        return redirect("/user_list/")

    # 查询所有的产品
    ret = models.Product.objects.all()
    return render(request, "add_user.html", {"product_list": ret})


# 删除用户
def delete_user(request):
    # 从URL里面取到要删除的用户id
    delete_id = request.GET.get("id")
    # 根据ID值取到要删除的用户对象,直接删除
    # 1. 去用户表把用户删了
    # 2. 去用户和产品的关联表,把对应的关联记录删除了
    models.User.objects.get(id=delete_id).delete()
    # 返回用户列表页面
    return redirect("/user_list/")


# 编辑用户
def edit_user(request):
    # 如果编辑完提交数据过来
    if request.method == "POST":
        # 拿到提交过来的编辑后的数据
        edit_user_id = request.POST.get("user_id")
        new_user_name = request.POST.get("user_name")
        # 拿到编辑后用户关联的产品信息
        new_product = request.POST.getlist("products")
        # 根据ID找到当前编辑的用户对象
        edit_user_obj = models.User.objects.get(id=edit_user_id )
        # 更新用户的名字
        edit_user_obj.name = new_user_name
        # 更新用户关联的产品的对应关系
        edit_user_obj.product.set(new_product)
        # 将修改提交到数据库
        edit_user_obj.save()
        # 返回用户列表页,查看是否编辑成功
        return redirect("/user_list/")

    # 从URL里面取要编辑的用户的id信息
    edit_id = request.GET.get("id")
    # 找到要编辑的用户对象
    edit_user_obj = models.User.objects.get(id=edit_id)

    # 查询所有的产品对象
    ret = models.Product.objects.all()
    return render(request, "edit_user.html", {"product_list": ret, "user": edit_user_obj})

