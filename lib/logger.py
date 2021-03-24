"""This code is based on Scott Punshon's Logger.js"""
import datetime


class Logger:
    COLORS = {
        "GREEN": '\033[1;32;48m',
        "YELLOW": '\033[1;33;48m',
        "RED": '\033[1;31;48m',
        "WHITE": '\033[0;48m',
        "END": '\033[1;37;0m'
    }

    SEVERITY = {
        "SUCCESS": "SUCCESS",
        "INFO": "INFO",
        "WARN": "WARN",
        "ERROR": "ERROR",
    }

    def __init__(self, module, indent_char='\t'):
        self.module = module.upper()
        self.indent_char = indent_char

    def format_msg(self, message, severity, i=0):
        indent = self.indent_char * i
        ts = datetime.datetime.now().isoformat()
        start = ""
        end = self.COLORS["END"]
        if severity == self.SEVERITY["SUCCESS"]:
            start = self.COLORS["GREEN"]
        elif severity == self.SEVERITY["WARN"]:
            start = self.COLORS["YELLOW"]
        elif severity == self.SEVERITY["ERROR"]:
            start = self.COLORS["RED"]
        elif severity == self.SEVERITY["INFO"]:
            start = self.COLORS["WHITE"]
        return f"{start}[{ts}][{self.module}][{severity}] {indent}{message}{end}"

    def info(self, message, indent=0):
        log_message = self.format_msg(message, self.SEVERITY["INFO"], indent)
        print(log_message)

    def success(self, message, indent=0):
        log_message = self.format_msg(message, self.SEVERITY["SUCCESS"], indent)
        print(log_message)

    def error(self, message, indent=0):
        log_message = self.format_msg(message, self.SEVERITY["ERROR"], indent)
        print(log_message)

    def warn(self, message, indent=0):
        log_message = self.format_msg(message, self.SEVERITY["WARN"], indent)
        print(log_message)
