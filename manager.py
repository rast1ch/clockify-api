import requests
import json
import tocken



class APIObject(object):
    """Class for working with clockify.me api
        On __init__ takes 3 arguments:
            - tocken - API tocken for authorisation
            - workspace - Workspace id
            - project - Project id"""
    def __init__(self, tocken, workspace, project):
        self.__tocken = tocken
        self.__headers = {'X-Api-Key':self.__tocken}

        self._workspace = workspace
        self._project = project

    
        

    def get_tasks(self):
        """
        Getting list of tasks from the given project
        """
        url = f'https://api.clockify.me/api/v1/workspaces/{self._workspace}/projects/{self._project}/tasks'
        r = requests.get(url=url, headers=self.__headers)
        responce = json.loads(r.content.decode('utf-8'))
        return responce

if __name__ == '__main__':
    a = APIObject(tocken=tocken.TOCKEN,
                  workspace=tocken.WORKSPACE_ID,
                  project=tocken.PROJECT_ID)
    a = a.get_tasks()
