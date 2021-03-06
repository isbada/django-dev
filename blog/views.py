import django
from django.shortcuts import get_object_or_404, render
from .models import Blog, BlogType
# ReadNum
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count

from read_statistics.utils import read_statistics_once_read


def get_blog_list_common_data(request, blogs_all_list):
    # 获取get请求参数,获取页码参数
    paginator = Paginator(blogs_all_list,
                          settings.EACH_PAGE_BLOGS_NUMBER)  # 每10页进行分页
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)  # get_page自动处理字符串 边界等问题
    # 原本的页码可能太多，只返回附近的
    current_page_num = page_of_blogs.number
    page_range = list(
        range(max(current_page_num - 2, 1),
              min(current_page_num + 2, paginator.num_pages) + 1))
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
    '''
    BlogType.objects.annotate(blog_count=Count('blog'))
    # 获取博客类型的数量, 并加入对象的属性
    blog_types = BlogType.objects.all()
    blog_type_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_type_list.append(blog_type)
    '''

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['page_range'] = page_range

    # 日期数量统计
    blog_dates = Blog.objects.dates('create_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year,
                                         create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    print(blog_dates_dict)
    context['blog_dates'] = blog_dates_dict
    return context


# Create your views here.
def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, id=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)

    context = {}
    context['previous_blog'] = Blog.objects.filter(
        create_time__gt=blog.create_time).last()
    context['next_blog'] = Blog.objects.filter(
        create_time__lt=blog.create_time).first()
    context['blog'] = blog

    # comments + django表单设置 (已经通过自定义标签实现)

    # 这里取出所有没有parent的评论作为返回值
    # blog_contet_type = ContentType.objects.get_for_model(blog)
    # comments = Comment.objects.filter(
    #     content_type=blog_contet_type, object_id=blog.pk, parent=None)
    # context['comments'] = comments.order_by('-comment_time')
    # data = {}
    # data['content_type'] = blog_contet_type.model
    # data['object_id'] = blog_pk
    # data['reply_comment_id'] = 0  # 回复id初始化为0
    # context['comment_form'] = CommentForm(initial=data)

    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')
    return response


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type

    return render(request, 'blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(create_time__year=year,
                                         create_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blogs_with_date'] = f"{year}年{month}月"
    context['blog_dates'] = Blog.objects.dates('create_time',
                                               'month',
                                               order='DESC')
    return render(request, 'blog/blogs_with_date.html', context)
