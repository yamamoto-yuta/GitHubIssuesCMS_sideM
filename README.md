# GitHubIssuesCMS_sideM
GitHub Issues driven Contents M@nagement System side Manager



# Setup

## sideF
1. Fork [sideF](https://github.com/ShotaroKataoka/GitHubIssuesCMS_sideF) (Can be named arbitrarily. Repository name will be your site URL.)
1. (Forked sideF Repository) Settings -> Actions -> General -> Workflow permissions -> check "Read and write permissions"

## sideM
1. Create a new **private** repository on Github. (Memo repository name; `{Your repository name}`)
1. `git clone --bare git@github.com:ShotaroKataoka/GitHubIssuesCMS_sideM.git ./{Your repository name}.git`  
   `cd {Your repository name}`  
   `git push --mirror git@github.com:<your_username>/{Your repository name}.git`
1. `cd ..`  
   `rm -rf {Your repository name}.git`
1. Setting Personal Access Token
    1. (Personal) Settings -> Developper settings -> Personal access tokens
    1. Generate New token
    1. Check `public_repo`
    1. Copy Token
1. Set token to your sideM repository secrets
    1. (Your sideM Repository) Settings -> Secrets -> Actions
    1. New repository secret
    2. Name: `API_TOKEN_GITHUB`, Value {Copied Personal Access Token}
    3. Add secret
1. `git clone <your_username>/{Your repository name}.git`  
   `cd ./{Your repository name}`
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
    1. Edit all values. (`root_url` will be known later, so this can be blank.)
    1. Create & Close issue.
    1. Wait sideM GitHub Actions end.

## sideF
1. Wait sideF GitHub Actions end. (This process may fail, but that is not a problem.)
1. (Your sideM Repository) Settings -> Pages -> Source branch `"build"` `"/(root)" `
1. Copy URL `Your site is ready to be published at {URL}`

## sideM
1. Edit Closed Profile issue.
    1. Set copied URL to `root_url`.
    1. Then, Reopen & Close this issue. 
    1. Wait sideM & sideF GitHub Actions end. (This process may fail, but that is not a problem.)
1. Create Your first post.
    1. New Issue & use "Article" template
    1. You can add `tag/` prefix labels to the issue; it become the article tags. (named `tag/{tag_name}` label will be article `{tag_name}` tag.)
    1. Write Issue markdown with YAML frontmatter & Close
    1. Wait sideM & sideF GitHub Actions end. (If this process succeeds, the article page is updated.)

# How to manage contents
## Post Articles
1. Create issue on sideM with `Article` (or `Reserved Article`) template.
1. Fill out YAML frontmatter follow a format.
1. Fill in the body text in markdown under YAML.
1. Clone issue and wait sideM & sideF GitHub Actions end.

## Edit Articles (or Profile)
1. Reopen the issue.
1. Edit the issue content.
1. Close the issue and wait sideM & sideF GitHub Actions end.
