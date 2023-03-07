class Custom_Exception(Exception):
    def __init__(self, status_code, msg: str):
        self.status_code = status_code
        self.msg = msg