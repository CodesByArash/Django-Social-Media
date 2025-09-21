from django.db import models
from .models import Post, Comment
from account.models import User


class PostRepository:
    """Repository for Post model operations"""
    
    @staticmethod
    def get_all_posts():
        """Get all posts ordered by creation time"""
        return Post.objects.all().order_by('-creation_time')
    
    @staticmethod
    def get_post_by_id(post_id):
        """Get a specific post by ID"""
        try:
            return Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_posts(user):
        """Get all posts by a specific user"""
        return Post.get_user_posts(user)
    
    @staticmethod
    def get_feed_posts(user):
        """Get posts for user's feed"""
        return Post.get_feed_posts(user)
    
    @staticmethod
    def create_post(user, image, caption=''):
        """Create a new post"""
        return Post.create_post(user, image, caption)
    
    @staticmethod
    def delete_post(post_id, user):
        """Delete a post if user is the owner"""
        post = PostRepository.get_post_by_id(post_id)
        if post:
            return post.delete_post(user)
        return False
    
    @staticmethod
    def like_post(post_id, user):
        """Like a post"""
        post = PostRepository.get_post_by_id(post_id)
        if post:
            return post.like_post(user)
        return False
    
    @staticmethod
    def unlike_post(post_id, user):
        """Unlike a post"""
        post = PostRepository.get_post_by_id(post_id)
        if post:
            return post.unlike_post(user)
        return False
    
    @staticmethod
    def toggle_like(post_id, user):
        """Toggle like/unlike status"""
        post = PostRepository.get_post_by_id(post_id)
        if post:
            return post.toggle_like(user)
        return False
    
    @staticmethod
    def get_posts_with_like_status(posts, user):
        """Get posts with like status for a user"""
        posts_with_likes = []
        for post in posts:
            is_liked = post.is_liked_by(user)
            posts_with_likes.append((post, is_liked))
        return posts_with_likes


class UserRepository:
    """Repository for User model operations"""
    
    @staticmethod
    def get_user_by_username(username):
        """Get user by username"""
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def search_users(query, exclude_user=None):
        """Search users by query"""
        queryset = User.objects.filter(username__icontains=query)
        if exclude_user:
            queryset = queryset.exclude(id=exclude_user.id)
        return queryset
    
    @staticmethod
    def follow_user(follower, user_to_follow):
        """Follow a user"""
        return follower.follow_user(user_to_follow)
    
    @staticmethod
    def unfollow_user(follower, user_to_unfollow):
        """Unfollow a user"""
        return follower.unfollow_user(user_to_unfollow)
    
    @staticmethod
    def toggle_follow(follower, user):
        """Toggle follow/unfollow status"""
        return follower.toggle_follow(user)
    
    @staticmethod
    def is_following(follower, user):
        """Check if follower is following user"""
        return follower.is_following(user)


class CommentRepository:
    """Repository for Comment model operations"""
    
    @staticmethod
    def get_post_comments(post):
        """Get all comments for a post"""
        return Comment.objects.filter(post=post).order_by('creation_time')
    
    @staticmethod
    def create_comment(post, user, text):
        """Create a new comment"""
        return Comment.objects.create(
            post=post,
            user=user,
            text=text
        )
    
    @staticmethod
    def delete_comment(comment_id, user):
        """Delete a comment if user is the owner"""
        try:
            comment = Comment.objects.get(id=comment_id)
            if comment.user == user:
                comment.delete()
                return True
        except Comment.DoesNotExist:
            pass
        return False
