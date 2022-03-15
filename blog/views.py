from django.shortcuts import render_to_response, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator
from django.conf import settings

# Create your views here.
def blog_list(request):

    # 获取get请求参数,获取页码参数
    page_num = request.GET.get('page', 1)
    blogs_all_list = Blog.objects.all()
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 每10页进行分页
    page_of_blogs = paginator.get_page(page_num)  # get_page自动处理字符串 边界等问题
    # 原本的页码可能太多，只返回附近的
    current_page_num = page_of_blogs.number
    page_range = list(
        range(max(current_page_num - 2, 1),
              min(current_page_num + 3, paginator.num_pages)))
    # 接上省略
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 接上首页尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range
    return render_to_response('blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog, id=blog_pk)
    return render_to_response('blog/blog_detail.html', context)


def blogs_with_type(request, blog_type_pk):
    context = {}

    # 获取get请求参数,获取页码参数
    page_num = request.GET.get('page', 1)
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 每10页进行分页
    page_of_blogs = paginator.get_page(page_num)  # get_page自动处理字符串 边界等问题
    # 原本的页码可能太多，只返回附近的
    current_page_num = page_of_blogs.number
    page_range = list(
        range(max(current_page_num - 2, 1),
              min(current_page_num + 2, paginator.num_pages) + 1))
    # 接上省略
    print(page_range, current_page_num, page_of_blogs)
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 接上首页尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['blog_type'] = blog_type
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range
    return render_to_response('blog/blogs_with_type.html', context)
