from django.db import transaction

from users.models import User
from django.contrib.auth.models import Group
from django.utils import timezone
from django.db.models import Count, F, Q, QuerySet, CharField, Transform
from typing import Iterable, List, Optional, Set, Tuple, Union, Dict
from users.lib.exceptions import (
    UserDoesNotExist,
    GroupDoesNotExist,
    UserWithGroupAlreadyExists,
    PlanDoesNotExist,
    SubscriptionDoesNotExist,
)


