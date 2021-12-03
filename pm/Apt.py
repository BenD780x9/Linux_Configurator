from typing import List
from .packages.Models.Package import Package
from .utils import run_cmd
import json


class Apt:
    def __init__(self) -> None:
        pass
    
    
    
    def load_packages() -> List[Package]:
        with open('./packages/apt.json') as f:
            data = json.load(f)
        return [Package(**p) for p in data]
        
    def install(pkg: Package):
        for command in pkg.commands:
            run_cmd(command)



