from src.article import article_build
from src.profile import profile_build
from models.issue import Issue
from const import ARTICLE_FLAG_LABEL, PROFILE_FLAG_LABEL


issue = Issue()

if issue.is_include([ARTICLE_FLAG_LABEL]):
    article_build()
elif issue.is_include([PROFILE_FLAG_LABEL]):
    profile_build()

