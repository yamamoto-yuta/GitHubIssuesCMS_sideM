import sys

from models.issue import Issue
from const import EXEC_WORKFLOW_FLAG_LABELS


issue = Issue()
if issue.is_include(EXEC_WORKFLOW_FLAG_LABELS):
    print('This includes PUBLISH FLAG')
    sys.exit(0)
else:
    print('This DO NOT includes PUBLISH FLAG')
    sys.exit(1)
