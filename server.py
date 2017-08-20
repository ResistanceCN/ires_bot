from github import Github


username = 'axionl'
token = 'a351ec7c8824e13b70b8f5cc62ed288de7f75794'
g = Github(username, token)
for repo in g.get_user().get_notification('axionl'):
    print(repo.name)
