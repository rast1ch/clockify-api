import requests
import datetime
import json
import tocken



class Interval(object):
    def __init__(self, time, task_id, date_start, date_end):
        self._task_id = task_id
        self.time = time[2:]
        self.time_start = date_start
        self.date_end = date_end

    
    

class Task(object):
    def __init__(self, name, id):
        self.name = name
        self._id = id
        self.interval = []
    
    def __str__(self):
        return self.name
    

    def add_interval(self, interval):
        self.interval.append(interval)
    

    def stdout(self):
        print(f'{self.name}\n--------------------')
        for i in self.interval:
            print(f'Working time ==> {i.time}')
        print("--------------------\n\n")

    



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
        
        self.tasks = []

    def get_tasks(self):
        """
        Getting list of tasks from the given project
        """
        url = f'https://api.clockify.me/api/v1/workspaces/{self._workspace}/projects/{self._project}/tasks'
        r = requests.get(url=url, headers=self.__headers)
        responce = json.loads(r.content.decode('utf-8'))
        task_list = []
        for task_raw in responce:
            task = Task(name=task_raw['name'], id=task_raw['id'])
            task_list.append(task)
        self.tasks = task_list

    def get_entries(self):
        url = f'https://api.clockify.me/api/v1/workspaces/{self._workspace}/user/6152d40de5f67d3511f21180/time-entries'
        r = requests.get(url=url, headers=self.__headers)
        time_parser = lambda x : datetime.datetime.strptime(str(x)[:10], '%Y-%m-%d')
        responce = json.loads(r.content.decode('utf-8'))
        for interval in responce:
            if interval['timeInterval']['duration'] != None:
                date_start = time_parser(interval['timeInterval']['start'])
                date_end = time_parser(interval['timeInterval']['end'])
                work = Interval(time=interval['timeInterval']['duration'],
                                task_id=interval['taskId'],
                                date_start=date_start,
                                date_end=date_end)
                for i in self.tasks:
                    if i._id == work._task_id:
                        i.add_interval(work)
        
        print(responce)



if __name__ == '__main__':
    task_list = []
    a = APIObject(tocken=tocken.TOCKEN,
                  workspace=tocken.WORKSPACE_ID,
                  project=tocken.PROJECT_ID)
    a.get_tasks()
    print(a.tasks)
    a.get_entries()
    for i in a.tasks:
        i.stdout()