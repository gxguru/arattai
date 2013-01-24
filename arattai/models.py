from django.db import models

#models for arattai blog
#here BlogModel is specified under quotes because of cross-reference. 
#Django threw an error that BlogModel is not defined. I did not want to predeclare
#or use different files for each models and import them. The quote works
class UserModel(models.Model):
	user_id=models.IntegerField(primary_key=True)
	display_name=models.CharField(max_length=20)
	first_name=models.CharField(max_length=20)
	last_name=models.CharField(max_length=20)
	email=models.CharField(max_length=20)
	blog_id=models.ForeignKey('BlogModel')

class BlogModel(models.Model):
	blog_id=models.IntegerField(primary_key=True)
	user_id=models.ForeignKey(UserModel)
	blog_name=models.CharField(max_length=20)
	content=models.TextField()
	date_created=models.DateField()

class CommentModel(models.Model):
	comment_id=models.IntegerField(primary_key=True)
	blog_id=models.ForeignKey(BlogModel)
	user_id=models.ForeignKey(UserModel)
	comment=models.TextField()
	date_created=models.DateField()
