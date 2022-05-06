#!/bin/bash
source ./settings.conf

# setup GitHub Actions workflow
workflow=$(cat ./templates/issue_builder.yml)
workflow=$(echo "$workflow" | sed -e "s/T_GITHUB_USER_NAME/${GITHUB_USER_NAME}/g")
workflow=$(echo "$workflow" | sed -e "s/T_GITHUB_USER_EMAIL/${GITHUB_USER_EMAIL}/g")
workflow=$(echo "$workflow" | sed -e "s/T_FRONTEND_REPOSITORY/${FRONTEND_REPOSITORY}/g")
if [ ! -d ./.github ]; then
    mkdir ./.github
fi
if [ ! -d ./.github/workflows ]; then
    mkdir ./.github/workflows
fi
if [ -e ./.github/workflows/issue_builder.yml ]; then
    read -p "cp: overwrite './.github/workflows/issue_builder.yml'? " prompt;
    if [ $prompt = 'y' ]; then
        echo "$workflow" >| ./.github/workflows/issue_builder.yml
    fi
else
    echo "$workflow" >| ./.github/workflows/issue_builder.yml
fi

# copy 
if [ ! -d ./.github/ISSUE_TEMPLATE ]; then
    mkdir ./.github/ISSUE_TEMPLATE
fi
cp -i ./templates/article.md ./.github/ISSUE_TEMPLATE/article.md
cp -i ./templates/article_reserve.md ./.github/ISSUE_TEMPLATE/article_reserve.md
cp -i ./templates/profile.md ./.github/ISSUE_TEMPLATE/profile.md
