#!/bin/bash
source ./settings.conf

# setup GitHub Actions workflow
workflow=$(cat ./templates/issue_builder.yml)
workflow=$(echo "$workflow" | sed -e "s/T_GITHUB_USER_NAME/${GITHUB_USER_NAME}/g")
workflow=$(echo "$workflow" | sed -e "s/T_GITHUB_USER_EMAIL/${GITHUB_USER_EMAIL}/g")
workflow=$(echo "$workflow" | sed -e "s/T_FRONTEND_REPOSITORY/${FRONTEND_REPOSITORY}/g")
if [ -e ./.github/workflows/issue_builder.yml ]; then
    echo './.github/workflows/issue_builder.yml already exists.'
    read -p "overwrite? (y/n) > " prompt;
    if [ $prompt = 'y' ]; then
        echo "$workflow" >| ./.github/workflows/issue_builder.yml
    fi
else
    echo "$workflow" >| ./.github/workflows/issue_builder.yml
fi


