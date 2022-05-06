#!/bin/bash
GITHUB_USER_NAME=$(git config user.name)
GITHUB_USER_EMAIL=$(git config user.email)

echo "#!/bin/bash" >| ./settings.conf
echo "GITHUB_USER_NAME='$GITHUB_USER_NAME'" >> ./settings.conf
echo "GITHUB_USER_EMAIL='$GITHUB_USER_EMAIL'" >> ./settings.conf
echo "FRONTEND_REPOSITORY='GitHubIssuesCMS_sideF'" >> ./settings.conf

