def renewal_rage_avg_when_post_new_review(sender, instance, created, **kwagrgs):
    from hotplace.models import (
        Place,
        Review,
    )
    if sender == Review:
        place = Place.objects.get(pk=instance.place.pk)
        try:
            place.rate_avg = sum([review.rate for review in place.reviews.all()]) / place.reviews.count()
            # TODO: annotate 등 사용해서 쿼리 리팩토링 할 수 있을듯
        except ZeroDivisionError:
            place.rate_avg = 0
        place.save()
