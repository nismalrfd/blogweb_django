from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse


from core.form import CommentForm, BlogForm
from core.models import BlogModel, Comment


# Create your views here.
from django.db.models import Q

def home(request):
    # Fetch all blogs, ordered by creation date
    blogs = BlogModel.objects.all().order_by('-created_at')
    
    # Fetch the latest post, if it exists
    latest_post = BlogModel.objects.latest('created_at') if BlogModel.objects.exists() else None
    
    # Handle the search functionality
    search_in = request.GET.get('q', '').strip()  # Fetch search query and remove extra spaces
    if search_in:
        # Search in title and content fields using Q objects for flexible matching
        blogs = BlogModel.objects.filter(
            Q(title__icontains=search_in) | Q(content__icontains=search_in)
        ).order_by('-created_at')

    # Context for rendering the template
    context = {
        'blogs': blogs,
        'latest_post': latest_post,
        'search_query': search_in,  # Pass the search query back to the template
    }
    return render(request, 'home.html', context)


def autocomplete(request):
    if 'term' in request.GET:
        qs=BlogModel.objects.filter(title__icontains=request.GET.get('term'))
        titles=list()
        for prodect in qs:
            titles.append(prodect.title)
            return JsonResponse(titles,safe=False)
    return render(request,'home.html')


def logout_page(request):
    logout(request)
    return redirect('/')


def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username').lower()
            password = request.POST.get('password')

            from django.contrib.auth.models import User
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.warning(request, 'User not Found ')
                return redirect('/login')
            # if not Profile.objects.filter(user = user_obj).first().is_verified:
            #     messages.warning(request, 'your profile not verified..')
            #     raise Exception('profile not verified')
            #
            user_obj = authenticate(username=username, password=password)

            if user_obj:
                login(request, user_obj)
                return redirect('/')

            messages.warning(request, 'wrong password ')
            return redirect('login')

        except Exception as e:
            messages.warning(request, 'Something went wrong')

    return render(request, 'login.html')


def register_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username').lower()
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')


            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.warning(request, 'username already exists')
                return redirect('/register')
            if confirm_password and password and password != confirm_password:
                messages.warning(request,'Password not match..')
                return redirect('/register')

            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()

            # Profile.objects.create(user= user_obj,token = genarate_random_string(20))


            messages.success(request, 'Account created')
            return redirect('login')
        except Exception as e:
            messages.warning(request, 'Something went wrong')

    return render(request, 'register.html')


def blog_details(request, id):
    try:
        blog_obj = BlogModel.objects.filter(id=id).first()
        comments = Comment.objects.filter(post=id)
        msg = False

        if request.user.is_authenticated:
            user = request.user

            if blog_obj.likes.filter(id=user.id).exists():
                msg = True

        if request.method == 'POST':

            if request.user.is_authenticated:
                user = request.user

                if blog_obj.likes.filter(id=user.id).exists():
                    blog_obj.likes.remove(user)
                    msg = False

                else:
                    blog_obj.likes.add(user)
                    msg = True
            else:
                return redirect('login_page')


            message = Comment.objects.create(
                name=request.user,
                post=blog_obj,
                body=request.POST.get('body')
            )

    except Exception as e:
        print(e)
    context = {'blog_obj': blog_obj,'comments':comments,'msg':msg}
    return render(request, 'blog_detail.html', context)

def see_blogs(request):
    blog_objs = BlogModel.objects.filter(user=request.user)
    context = {
        'blog_objs': blog_objs
    }
    return render(request, 'see_blog.html', context)



#
# def add_blog(request):
#     context = {'form': BlogForm}
#     try:
#         if request.method == 'POST':
#             form = BlogForm(request.POST)
#             image = request.FILES.get('image')
#             print(request.FILES)
#             title = request.POST.get('title')
#             user = request.user
#
#             if form.is_valid():
#                 print('Valid')
#                 content = form.cleaned_data['content']
#
#             blog_obj = BlogModel.objects.create(
#                 user=user, title=title,
#                 content=content, image=image
#             )
#             print(blog_obj)
#             return redirect('/add-blog')
#     except Exception as e:
#         print(e)
#
#     return render(request, 'add_blog.html', context)


def add_blog(request):
    if request.user.is_authenticated:
        user = request.user
        form = BlogForm()
        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES)
            if form.is_valid():
                new = form.save(commit=False)
                new.user = user
                new.save()
                form.save()
                messages.success(request,'added...')
                print('valid')
                return redirect('/')
    context = {'form': form}
    return render(request, 'add_blog.html', context)



def delete_blog(request, id):
    blog_obj = BlogModel.objects.get(id=id)

    if blog_obj.user == request.user:
        blog_obj.delete()
    return redirect('/see-blogs')


#
# def update_blog(request, slug):
#     context = {}
#     blog_obj = BlogModel.objects.get(slug=slug)
#
#     if blog_obj.user != request.user:
#         return redirect('/')
#
#     form = BlogForm(instance=blog_obj)
#     if request.method == 'POST':
#         form = BlogForm(request.POST,instance=blog_obj)
#         print(request.FILES)
#         image = request.FILES['image']
#         title = request.POST.get('title')
#         user = request.user
#
#         if form.is_valid():
#             content = form.cleaned_data['content']
#
#         blog_obj = BlogModel.objects.create(
#             user=user, title=title,
#                 content=content, image=image
#         )
#     context['blog_obj'] = blog_obj
#     context['form'] = form
#     return render(request, 'update_blog.html', context)

def update_blog(request, id):
    blog_obj = BlogModel.objects.get(id=id)
    form = BlogForm(instance=blog_obj)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog_obj)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'update_blog.html', context)

from django.http import JsonResponse

def search_view(request):
    query = request.GET.get('q')
    results = BlogModel.objects.filter(title__icontains=query)
    data = [{'title': item.title, 'description': item.description} for item in results]
    return JsonResponse(data, safe=False)
