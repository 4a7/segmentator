from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def login(self):
        self.client.post("/login", {"username":"rodrigo@ucr.ac.cr", "password":"pwd-de-rodrigo"})

    @task(2)
    def index(self):
        self.client.get("/index")
        
    @task(1)
    def segmentar(self):
        self.client.get("/segmentar2")
    @task(3)
    def cargar(self):
        self.client.get("/cargar")

    @task(4)
    def visualizar(self):
        self.client.get("/visualizar")

    @task(5)
    def segmentadas(self):
        self.client.get("/segmentadas")
        
    @task(6)
    def exito(self):
        self.client.get("/exito")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000