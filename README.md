# GitHubIssuesCMS_sideM
GitHub Issues driven Contents M@nagement System side Manager



# Setup

## sideF
1. Fork [sideF](https://github.com/ShotaroKataoka/GitHubIssuesCMS_sideF) (Can be named arbitrarily. Repository name will be your site URL.)
1. (Forked Repository) Settings -> Actions -> General -> Workflow permissions -> check "Read and write permissions"

## sideM
1. Fork this repository (Can be named arbitrarily.)
1. Setting Personal Access Token
    1. (Personal) Settings -> Developper settings -> Personal access tokens
    1. Generate New token
    1. Check `public_repo`
    1. Copy Token
1. Set token to sideM secrets
    1. (Forked Repository) Settings -> Secrets -> Actions
    1. New repository secret
    2. Name: API_TOKEN_GITHUB, Value {Personal Access Token}
    3. Add secret
1. Clone forked sideM repository
1. Exec `./init_config.sh`
1. Edit `settings.config`
1. Exec `./setup.sh`
1. Exec `git add .`
1. Exec `git commit -m 'exec first setup.sh'`
1. Exec `git push origin main` (push to main branch of your repository)
1. Setting Labels on Forked sideM Repository.
    1. Create `article` and `profile` labels.
1. Create&Edit&Close Profile Issue on Forked sideM Repository.
    1. New Issue & use "Profile" template
    1. Edit all values. (`root_url` will be known later), so this can be blank.
    1. Create & Close issue.
    1. Wait Actions end.

## sideF
1. Wait Actions end.
1. (Forked Repository) Settings -> Pages -> Source branch "build" "/(root)" 
1. Copy URL `Your site is ready to be published at {URL}`

## sideM
1. Edit Closed Profile issue.
    1. Set copied URL to `root_url`.
1. Create Your first post.
    1. New Issue & use "Article" template
    1. You can add label as article tag. (named `tag/{tag_name}` label will be article tag.)
    1. Write Issue markdown with yaml frontmatter & Close
