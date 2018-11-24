from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from goods.models import Index_run_jpg, Index_active_list, Index_active_area


def show(request):
    # 显示轮播的图片,从数据库中进行查取并显示到页面
    run_jpg = Index_run_jpg.objects.get(pk=6).jpg_address
    # 查询出对应
    active_jpg = Index_active_list.objects.all().order_by('pk')[:6]
    # 专区列表查询并查询出对应的商品
    # 查询出.首页专区的名称列表
    active_area = Index_active_area.objects.all()
    # 因为是个查询集合,所以需要进行遍历进一步查询
    # data = {}
    # for i in active_area:
    #     data['{}'.format(i.name)] = ''
    #     for j in i.active_goods_set.all():
    #         j.link_SKU.all()

    context = {
        'jpg':run_jpg,
        'active_jpg':active_jpg,
        'active_area':active_area,
    }
    return render(request,'goods/index.html',context=context)