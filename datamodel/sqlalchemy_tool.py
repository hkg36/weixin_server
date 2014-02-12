__author__ = 'amen'
from sqlalchemy.orm import Session
class AutoSession(Session):
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()