from rest_framework import routers

from shore.alert import views


class OptionalTrailingSlashRouter(routers.DefaultRouter):
    """ A router which allows endpoints with or without trailing slashes. """

    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'


router = OptionalTrailingSlashRouter()

router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'subscriptions', views.SubscriptionViewSet, basename='subscription')

urlpatterns = router.urls
