import pytest
import requests
from lesson8.pages.project_page import ProjectPage
from lesson8.config import BASE_URL, HEADERS


class TestProjects:
    def setup_method(self):
        self.project_page = ProjectPage()
        self.test_project_title = "Тестовый проект"

    def teardown_method(self):
        pass

    def test_create_project_positive(self):
        resp = self.project_page.create_project("Лекция 8")
        assert resp.status_code == 201, f"Ожидался код 201, получен {resp.status_code}"

        project_id = self.project_page.get_project_id_from_response(resp)
        assert project_id is not None, "ID проекта не получен"

        print(f"Создан проект с ID: {project_id}")
        print(f"Ответ: {resp.json()}")

    def test_get_project_positive(self):
        create_resp = self.project_page.create_project("Проект для получения")
        assert create_resp.status_code == 201

        project_id = self.project_page.get_project_id_from_response(create_resp)

        get_resp = self.project_page.get_project(project_id)

        assert get_resp.status_code == 200
        assert get_resp.json()['id'] == project_id
        print(f"Получен проект: {get_resp.json()}")

    def test_update_project_positive(self):
        create_resp = self.project_page.create_project("Лекция 8")
        assert create_resp.status_code == 201

        project_id = self.project_page.get_project_id_from_response(create_resp)
        new_title = "Лекция 888"

        update_resp = self.project_page.update_project(project_id, title=new_title)

        assert update_resp.status_code == 200

        get_resp = self.project_page.get_project(project_id)
        assert get_resp.json()['title'] == new_title
        print(f"Проект обновлен: {get_resp.json()}")

    def test_create_project_negative_empty_title(self):
        resp = self.project_page.create_project("")

        assert resp.status_code in [400], \
            f"Ожидался код ошибки, получен {resp.status_code}"
        print(f"Ошибка при создании: {resp.status_code} - {resp.text}")

    def test_create_project_negative_no_title(self):
        url = f"{BASE_URL}/projects"
        body = {}

        resp = requests.post(url, json=body, headers=HEADERS)

        assert resp.status_code in [400]
        print(f"Ошибка при создании: {resp.status_code} - {resp.text}")

    def test_get_project_negative_not_found(self):
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        resp = self.project_page.get_project(non_existent_id)

        assert resp.status_code == 404
        print(f"Проект не найден: {resp.status_code}")

    def test_update_project_negative_not_found(self):
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        resp = self.project_page.update_project(non_existent_id, title="Новое название")

        assert resp.status_code == 404
        print(f"Обновление несуществующего проекта: {resp.status_code}")

    def test_update_project_negative_empty_payload(self):
        create_resp = self.project_page.create_project("Проект для теста")
        assert create_resp.status_code == 201

        project_id = self.project_page.get_project_id_from_response(create_resp)

        url = f"{BASE_URL}/projects/{project_id}"
        resp = requests.put(url, json={}, headers=HEADERS)

        assert resp.status_code in [400]
        print(f"Ошибка при обновлении: {resp.status_code} - {resp.text}")