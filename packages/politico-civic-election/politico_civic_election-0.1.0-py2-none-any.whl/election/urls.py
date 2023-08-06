from django.urls import include, path
from rest_framework import routers

from .viewsets import (BallotAnswerViewSet, BallotMeasureViewSet,
                       CandidateViewSet, ElectionCycleViewSet,
                       ElectionDayViewSet, ElectionTypeViewSet,
                       ElectionViewSet, RaceViewSet)

router = routers.DefaultRouter()

router.register(r'ballot-answers', BallotAnswerViewSet)
router.register(r'ballot-measures', BallotMeasureViewSet)
router.register(r'candidates', CandidateViewSet)
router.register(r'election-cycles', ElectionCycleViewSet)
router.register(r'election-days', ElectionDayViewSet)
router.register(r'election-types', ElectionTypeViewSet)
router.register(r'elections', ElectionViewSet)
router.register(r'races', RaceViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
