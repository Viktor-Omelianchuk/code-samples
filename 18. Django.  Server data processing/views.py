import json

from django import forms
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator

from .models import Item, Review


class GoodForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(max_length=1024)
    price = forms.IntegerField(min_value=1, max_value=1000000)


class ReviewForm(forms.Form):
    text = forms.CharField(max_length=1024)
    grade = forms.IntegerField(min_value=1, max_value=10)


@method_decorator(csrf_exempt, name="dispatch")
class AddItemView(View):
    """View to create a product."""

    def post(self, request):
        try:
            data = json.loads(request.body)
            if isinstance(data["title"], int) or isinstance(data["description"], int):
                return JsonResponse(status=400, data={})
            form = GoodForm(data)
        except:
            return JsonResponse(status=400, data={})
        if form.is_valid():
            cd = form.cleaned_data
            n = Item(**cd)
            n.save()
            return JsonResponse(status=201, data={"id": n.id})
        return JsonResponse(status=400, data={})


@method_decorator(csrf_exempt, name="dispatch")
class PostReviewView(View):
    """View to create product reviews."""

    def post(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return JsonResponse(status=404, data={})
        try:
            data = json.loads(request.body)
            if isinstance(data["text"], int):
                return JsonResponse(status=400, data={})
            form = ReviewForm(data)
        except:
            return JsonResponse(status=400, data={})
        if form.is_valid():
            cd = form.cleaned_data
            cd["item"] = item
            n = Review(**cd)
            n.save()
            return JsonResponse(status=201, data={"id": n.id})
        return JsonResponse(status=400, data={})


class GetItemView(View):
    """View for product information."""

    def get(self, request, item_id):
        try:
            item = Item.objects.prefetch_related("review_set").get(id=item_id)
        except Item.DoesNotExist:
            return JsonResponse(status=404, data={})
        item_dict = model_to_dict(item)
        item_reviews = [model_to_dict(x) for x in item.review_set.all()]
        item_reviews = sorted(
            item_reviews, key=lambda review: review["id"], reverse=True
        )[:5]
        for review in item_reviews:
            review.pop("item", None)
        item_dict["reviews"] = item_reviews
        return JsonResponse(item_dict, status=200)
