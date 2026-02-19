# pages/project_page.py
import requests
from lesson8.config import BASE_URL, HEADERS



class ProjectPage:
    """Page Object для работы с проектами Yougile."""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS
        self.projects_url = f"{self.base_url}/projects"
    
    def create_project(self, title):
        """Создание нового проекта."""
        body = {"title": title}
        resp = requests.post(
            self.projects_url, 
            json=body, 
            headers=self.headers
        )
        return resp
    
    def get_project(self, project_id):
        """Получение проекта по ID."""
        url = f"{self.projects_url}/{project_id}"
        resp = requests.get(url, headers=self.headers)
        return resp
    
    def update_project(self, project_id, title=None, deleted=None):
        """Обновление проекта."""
        url = f"{self.projects_url}/{project_id}"
        body = {}
        if title:
            body["title"] = title
        if deleted is not None:
            body["deleted"] = deleted
        
        resp = requests.put(url, json=body, headers=self.headers)
        return resp
    
    def get_project_id_from_response(self, response):
        """Извлечение ID проекта из ответа."""
        return response.json().get('id')
    
    def get_project_title_from_response(self, response):
        """Извлечение названия проекта из ответа."""
        return response.json().get('title')