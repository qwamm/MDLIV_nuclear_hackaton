# import jira
import httpx
import requests
from jira_env import TOKEN

# oauth_dict = {
#     'access_token': TOKEN,
#     'consumer_key': "kpZForY3FmJ5SerZaGZnKf3Kz5I6qF4s",
#     'consumer_secret': "ATOATNDEGnmgm2oRwRDIJPpWgUA_ghPro4Ho2GTADYbW6BgQJsYIG75cm0bzdEZ9VdaD3FDCC732",
#     'key_cert': None,
#     'access_token_secret': None
# }
# client=jira.JIRA(server="https://mdliv2024.atlassian.net", oauth=oauth_dict)
# print(client.client_info())

def get_jira_data(url, access_token):
  headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
  }

  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    return response.json()
  else:
    print(f"Error fetching Jira data: {response.status_code}, {response.text}")
    return None

#data and permissions
response=httpx.get("https://api.atlassian.com/oauth/token/accessible-resources", headers=
{
    'Authorization': f'Bearer {TOKEN}',
    'Accept': 'application/json'
})
print(response.json())

jira_url = "https://api.atlassian.com/ex/jira/c933a17d-f53d-42d4-8c05-18fef872720f/rest/api/2/project"
#jira_url = "https://mdliv2024.atlassian.net/rest/agile/1.0/board/1"
#project format in jira:
#[{'expand': 'description,lead,issueTypes,url,projectKeys,permissions,insight', 'self': 'https://api.atlassian.com/ex/jira/c933a17d-f53d-42d4-8c05-18fef872720f/rest/api/2/project/10000', 'id': '10000', 'key': 'SCRUM', 'name': 'aboutGG', 'avatarUrls': {'48x48': 'https://api.atlassian.com/ex/jira/c933a17d-f53d-42d4-8c05-18fef872720f/rest/api/2/universal_avatar/view/type/project/avatar/10419', '24x24': 'https://api.atlassian.com/ex/jira/c933a17d-f53d-42d4-8c05-18fef872720f/rest/api/2/universal_avatar/view/type/project/avatar/10419?size=small', '16x16': 'https://api.atlassian.com/ex/jira/c933a17d-f53d-42d4-8c05-18fef872720f/rest/api/2/universal_avatar/view/type/project/avatar/10419?size=xsmall', '32x32': 'https://api.atlassian.com/ex/jira/c933a17d-f53d-42d4-8c05-18fef872720f/rest/api/2/universal_avatar/view/type/project/avatar/10419?size=medium'}, 'projectTypeKey': 'software', 'simplified': True, 'style': 'next-gen', 'isPrivate': False, 'properties': {}, 'entityId': 'c831bde8-251a-49ed-968c-291d840e701f', 'uuid': 'c831bde8-251a-49ed-968c-291d840e701f'}]
data=get_jira_data(jira_url, TOKEN)
print(data)