import requests
from json import JSONDecodeError
import logging


class ApiClient:
    def __init__(self, api_url=None, api_token=None):
        self.api_url = api_url
        self.headers = {}

        if api_token is not None:
            self.headers["Authorization"] = "Bearer " + api_token

    def call(self, method, url, files={}, data={}):
        if self.api_url is None:
            raise RuntimeError("The API URL is not configured")

        return requests.request(method, self.api_url + "/v1/" + url, files=files, json=data, headers=self.headers)

    def post(self, url, files={}, data={}):
        return self.extract_payload(self.call("post", url, files, data))

    def get(self, url):
        return self.extract_payload(self.call("get", url))

    def get_status(self):
        return self.call("get", "").json()

    def get_runtime_environments(self):
        return self.get("/runtime-environments")

    def get_pipelines(self):
        return self.get("/pipelines")

    def get_exercise(self, exercise_id):
        return self.get("/exercises/{}".format(exercise_id))

    def get_exercises(self):
        return self.get("/exercises")

    def get_reference_solutions(self, exercise_id):
        return self.get("/reference-solutions/exercise/{}".format(exercise_id))

    def get_reference_solution_evaluations(self, solution_id):
        return self.get("/reference-solutions/{}/evaluations".format(solution_id))

    def upload_file(self, filename, stream):
        return self.post("/uploaded-files", files={"file": (filename, stream)})

    def get_uploaded_file_data(self, file_id):
        return self.get("/uploaded-files/{}".format(file_id))

    def create_exercise(self, group_id):
        return self.post("/exercises", data={
            "groupId": group_id
        })

    def add_exercise_attachments(self, exercise_id, file_ids):
        self.post("/exercises/{}/attachment-files".format(exercise_id), data={"files": file_ids})

    def get_exercise_attachments(self, exercise_id):
        return self.get("/exercises/{}/attachment-files".format(exercise_id))

    def add_exercise_files(self, exercise_id, file_ids):
        self.post("/exercises/{}/supplementary-files".format(exercise_id), data={"files": file_ids})

    def get_exercise_files(self, exercise_id):
        return self.get("/exercises/{}/supplementary-files".format(exercise_id))

    def set_exercise_score_config(self, exercise_id, score_config: str):
        return self.post("/exercises/{}/score-config".format(exercise_id), data={"scoreConfig": score_config})

    def update_exercise(self, exercise_id, details):
        self.post('/exercises/{}'.format(exercise_id), data=details)

    def create_reference_solution(self, exercise_id, data):
        return self.post('/reference-solutions/exercise/{}/submit'.format(exercise_id), data=data)

    def update_environment_configs(self, exercise_id, configs):
        self.post("/exercises/{}/environment-configs".format(exercise_id), data={
            "environmentConfigs": configs
        })

    def update_exercise_config(self, exercise_id, config):
        self.post("/exercises/{}/config".format(exercise_id), data={"config": config})

    def set_exercise_tests(self, exercise_id, tests):
        self.post("/exercises/{}/tests".format(exercise_id), data={"tests": tests})

    def get_exercise_tests(self, exercise_id):
        return self.get("/exercises/{}/tests".format(exercise_id))

    def update_limits(self, exercise_id, environment_id, hwgroup_id, limits):
        self.post("/exercises/{}/environment/{}/hwgroup/{}/limits".format(exercise_id, environment_id, hwgroup_id),
                  data={"limits": limits})

    def evaluate_reference_solutions(self, exercise_id):
        self.post("/reference-solutions/exercise/{}/evaluate".format(exercise_id), data={})

    def get_hwgroups(self):
        return self.get("/hardware-groups")

    def login(self, username, password):
        return self.post("/login", data={
            "username": username,
            "password": password
        })

    def login_external(self, service_id, auth_type, credentials):
        return self.post("/login/{}/{}".format(service_id, auth_type), data=credentials)

    @staticmethod
    def extract_payload(response):
        try:
            json = response.json()
        except JSONDecodeError:
            logging.error("Loading JSON response failed, see full response below:")
            logging.error(response.text)
            raise RuntimeError("Loading JSON response failed")

        if not json["success"]:
            raise RuntimeError("Received error from API: " + json["msg"])

        return json["payload"]

