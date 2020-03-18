def basicauth(view_func):
    """Decorator implementing HTTP Basic AUTH."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == 'basic':
                    token = base64.b64decode(auth[1].encode('ascii'))
                    username, password = token.decode('utf-8').split(':')
                    user = authenticate(username=username, password=password)
                    if user is not None and user.is_active:
                        request.user = user
                        return view_func(request, *args, **kwargs)

        response = HttpResponse(status=401)
        response['WWW-Authenticate'] = 'Basic realm="Somemart staff API"'
        return response
    return _wrapped_view


def staff_required(view_func):
    """Decorator checking the presence of the is_staff flag for the user."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        response = HttpResponse(status=403)
        return response
    return _wrapped_view


from django.utils.decorators import method_decorator


@method_decorator(basicauth, name='dispatch')
@method_decorator(staff_required, name='dispatch')
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


@method_decorator(basicauth, name='dispatch')
@method_decorator(staff_required, name='dispatch')
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
    