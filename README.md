# GitHubIssuesCMS_sideM
GitHub Issues driven Contents Management System side Manager



# Setup

## sideF
1. Fork [sideF](https://github.com/ShotaroKataoka/GitHubIssuesCMS_sideF)
1. Settings -> Actions -> General -> Workflow permissions -> check "Read and write permissions"
1. Setup sideF

## sideM
1. Fork this repository (Can be named arbitrarily)
1. Setting Personal Access Token
  1. Settings
  1. Developper settings
  1. Personal access tokens
  1. Generate New token
  1.  `public_repo`
  1. check `public_repo`
  1. Copy Token
1. Set token to sideM secrets
  1. 
1. Clone forked sideM repository
1. Exec `./init_config.sh`
1. Edit `settings.config`
1. Exec `./setup.sh`
1. Exec `git add .`
1. Exec `git commit -m 'exec first setup.sh'`
1. Exec `git push origin main` (push to main branch of your repository)
1. Setting Labels on GitHub Repository.
  1. Create `article` and `profile` labels.
