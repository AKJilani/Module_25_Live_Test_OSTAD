from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseRedirect
from .models import Post, UserProfile, Like, Comment, Share
from .forms import CustomUserCreationForm, PostForm, CommentForm, UserProfileForm
from django.contrib.auth import logout
from django.db.models import Count, Q
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'social_app/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

class HomeListView(ListView):
    model = Post
    template_name = 'social_app/home.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_template_names(self):
        if not self.request.user.is_authenticated:
            return ['social_app/landing.html']
        return ['social_app/home.html']
    
    def get_queryset(self):
        queryset = Post.objects.all().select_related('user')
        
        # Date filtering
        date_filter = self.request.GET.get('date_filter')
        if date_filter == 'oldest':
            queryset = queryset.order_by('created_at')
        else:  # newest or default
            queryset = queryset.order_by('-created_at')
            
        # Media type filtering
        media_type = self.request.GET.get('media_type')
        if media_type == 'text_only':
            queryset = queryset.filter(image='')
        elif media_type == 'images':
            queryset = queryset.exclude(image='')
            
        # User filtering
        username = self.request.GET.get('username')
        if username:
            queryset = queryset.filter(user__username=username)
            
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(content__icontains=search_query) |
                Q(user__username__icontains=search_query)
            )
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add filter parameters to context for maintaining state in template
        context['date_filter'] = self.request.GET.get('date_filter', 'newest')
        context['media_type'] = self.request.GET.get('media_type', '')
        context['username_filter'] = self.request.GET.get('username', '')
        context['search_query'] = self.request.GET.get('search', '')
        # Add list of users for the user filter dropdown
        context['users'] = User.objects.all()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'social_app/post_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'social_app/post_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'social_app/post_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user
        
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)

@login_required
def profile(request, username=None):
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user
    
    # Get base querysets
    posts_queryset = Post.objects.filter(user=profile_user).select_related('user')
    shared_posts = Share.objects.filter(user=profile_user).select_related('original_post', 'original_post__user')
    
    # Apply filters
    date_filter = request.GET.get('date_filter')
    if date_filter == 'oldest':
        posts_queryset = posts_queryset.order_by('created_at')
        shared_posts = shared_posts.order_by('created_at')
    else:  # newest or default
        posts_queryset = posts_queryset.order_by('-created_at')
        shared_posts = shared_posts.order_by('-created_at')
    
    # Media type filtering
    media_type = request.GET.get('media_type')
    if media_type == 'text_only':
        posts_queryset = posts_queryset.filter(image='')
    elif media_type == 'images':
        posts_queryset = posts_queryset.exclude(image='')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        posts_queryset = posts_queryset.filter(content__icontains=search_query)
        shared_posts = shared_posts.filter(
            Q(original_post__content__icontains=search_query) |
            Q(comment__icontains=search_query)
        )
    
    # Get or create profile
    profile, created = UserProfile.objects.get_or_create(user=profile_user)
    
    # Handle profile edit
    if request.method == 'POST' and request.user == profile_user:
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts_queryset,
        'shared_posts': shared_posts,
        'profile_form': profile_form,
        'is_own_profile': request.user == profile_user,
        'date_filter': date_filter or 'newest',
        'media_type': media_type or '',
        'search_query': search_query or ''
    }
    
    return render(request, 'social_app/profile.html', context)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        # User already liked the post, so unlike it
        like.delete()
        action = 'unliked'
    else:
        action = 'liked'
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # AJAX request
        return JsonResponse({
            'action': action,
            'like_count': post.like_count
        })
    else:
        # Regular request
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('home')))

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # AJAX request
                return JsonResponse({
                    'status': 'success',
                    'comment_id': comment.id,
                    'username': comment.user.username,
                    'content': comment.content,
                    'created_at': comment.created_at.strftime('%b %d, %Y, %I:%M %p')
                })
            
            messages.success(request, 'Comment added successfully!')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('home')))

@login_required
def share_post(request, post_id):
    original_post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        comment = request.POST.get('share_comment', '')
        share = Share.objects.create(
            user=request.user,
            original_post=original_post,
            comment=comment
        )
        messages.success(request, 'Post shared successfully!')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('home')))

@login_required
def user_profile_edit(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'social_app/profile_edit.html', {'form': form})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    
    if request.method == 'POST':
        comment.delete()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)