import github as pygit
import datetime

#to be replaced by data from db
USER_LOGIN="kargamant"
USER_TOKEN="ghu_V4SPHsWyPv4iYc0fMyYWInnEWoFoai39fZMi"
REPO_NAME="kargamant/tst_gh_app"

#activation
auth=pygit.Auth.Token(USER_TOKEN)
user_github=pygit.Github(auth=auth)
#if token is incorrect than throw github.GithubException.BadCredentialsException

#data preps
user_activity_data={
    'commits_on_previous_week': 0,
    'pull_requests_on_previous_week': 0,
    'comments_on_previous_week': 0
}
today=datetime.datetime.now()
user_name=user_github.get_user(USER_LOGIN).name
repo=user_github.get_repo(REPO_NAME)
comments_ids=set()
commits_sha=set()
pulls_ids=set()

#counting
for br in repo.get_branches():
    for commit in repo.get_commits(sha=br.commit.sha):
        if commit.committer is None or commit.sha in commits_sha:
            continue

        if commit.commit.author.name==user_name:
            commit_date = commit.commit.committer.date.replace(tzinfo=None)
            user_activity_data['commits_on_previous_week']+=((today-commit_date).days<=7)
            commits_sha.add(commit.sha)

        for comment in commit.get_comments():
            if comment.id in comments_ids:
                continue
            if comment.user.name==user_name:
                comment_date=comment.created_at.replace(tzinfo=None)
                user_activity_data['comments_on_previous_week']+=((today-comment_date).days<=7)
                comments_ids.add(comment.id)
for pull in repo.get_pulls():
    if pull.user is None or pull.id in pulls_ids:
        continue
    if pull.user.name==user_name:
        pull_date=pull.created_at.replace(tzinfo=None)
        user_activity_data['pull_requests_on_previous_week']+=((today-pull_date).days<=7)
        pulls_ids.add(pull.id)
print(user_activity_data)
user_github.close()
