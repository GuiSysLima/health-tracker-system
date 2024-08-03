import threading
import time
from django.apps import AppConfig

class SmartwatchesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smartwatches'

    def start_thread(self):
        from .views import  atualizar_todos_smartwatches
        thread = threading.Thread(target=atualizar_todos_smartwatches,args=(5000,5020))
        thread.daemon = True
        thread.start()

    def ready(self):
        self.start_thread()
