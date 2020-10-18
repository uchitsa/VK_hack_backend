import json
from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from tortoise.functions import Count


class Region(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50)


class City(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50)
    area = fields.CharField(max_length=50, null=True, default=True)
    region = fields.CharField(max_length=50, null=True, default=True)


class User(models.Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=250)
    last_login = fields.DatetimeField(auto_now_add=True)
    is_admin = fields.BooleanField(default=False)
    city = fields.ForeignKeyField('models.City', related_name='users',
                                  on_delete=fields.SET_NULL, null=True, default=None)
    region = fields.ForeignKeyField('models.Region', related_name='users',
                                    on_delete=fields.SET_NULL, null=True, default=None)


class Category(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=60)


class Host(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=200)


class Source(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=250)
    host = fields.ForeignKeyField('models.Host', related_name='sources', on_delete=fields.CASCADE)
    url = fields.CharField(max_length=500)
    city = fields.ForeignKeyField('models.City', related_name='sources', on_delete=fields.CASCADE,
                                  default=None, null=True)


class PotentialPost(models.Model):
    id = fields.BigIntField(pk=True)
    text = fields.CharField(max_length=1500, null=True, default=None)
    video = fields.CharField(max_length=500, null=True, default=None)
    photo = fields.CharField(max_length=500, null=True, default=None)
    url = fields.CharField(max_length=500, null=True, default=None)
    source = fields.ForeignKeyField('models.Source', related_name='potential_posts', on_delete=fields.CASCADE)
    added = fields.DatetimeField(auto_now=True)
    category = fields.ForeignKeyField('models.Category', related_name='potential_posts', on_delete=fields.CASCADE)
    is_new = fields.BooleanField(default=False)


class Post(models.Model):
    id = fields.BigIntField(pk=True)
    post = fields.OneToOneField('models.PotentialPost', related_name='post', on_delete=fields.CASCADE)
    time = fields.DatetimeField(auto_now=True)
    user = fields.ForeignKeyField('models.User', related_name='posts', on_delete=fields.SET_NULL, null=True, default=None)


class Bookmark(models.Model):
    id = fields.BigIntField(pk=True)
    post = fields.ForeignKeyField('models.Post', related_name='bookmarks', on_delete=fields.CASCADE)
    user = fields.ForeignKeyField('models.User', related_name='bookmarks', on_delete=fields.CASCADE)
    time = fields.DatetimeField(auto_now=True)


UserPydantic = pydantic_model_creator(User, name="User")
UserInPydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
UserPydanticList = pydantic_queryset_creator(User)

CityPydantic = pydantic_model_creator(City, name="City")
CityPydanticList = pydantic_queryset_creator(City)

RegionPydantic = pydantic_model_creator(Region, name="Region")
RegionPydanticList = pydantic_queryset_creator(Region)

CategoryPydantic = pydantic_model_creator(Category, name="Category")
CategoryPydanticList = pydantic_queryset_creator(Category)

PotentialPostPydantic = pydantic_model_creator(PotentialPost, name="PotentialPost")
PotentialPostPydanticList = pydantic_queryset_creator(PotentialPost)
