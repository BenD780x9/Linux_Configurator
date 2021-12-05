from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class Package(BaseModel):
    name: str
    description: str
    commands: List
    high_privilege: bool
    pre_update: bool
    pre_upgrade: bool
    upgrade: bool
    
    
