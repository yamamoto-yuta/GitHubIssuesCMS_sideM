""" transform issue to profile data

issue id           -> None
issue title        -> None
issue body         -> Parse yaml & build "consts/profile.json"
issue labels       -> None
issue closed_at    -> None
"""

from models.issue import Issue
from models.profile import Profile

def profile_build():
    # load issue
    issue = Issue()

    profile = Profile.load_profile()
    if profile is None:
        profile = Profile()

    profile.set_profile(issue.body)

    profile.save()

