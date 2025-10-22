from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class MissionRoom(BaseModel):
    """Representa uma sala/área da missão"""
    id: str
    name: str
    description: str
    enemies: List[Dict[str, Any]] = []
    treasures: List[Dict[str, Any]] = []
    exits: Dict[str, str]  # direção: id_da_sala
    visited: bool = False

class Mission(BaseModel):
    """Representa uma missão completa"""
    id: str
    name: str
    description: str
    difficulty: str
    min_level: int
    rewards: Dict[str, Any]
    rooms: Dict[str, MissionRoom]
    starting_room: str

class MissionProgress(BaseModel):
    """Progresso do personagem na missão"""
    character_name: str
    mission_id: str
    current_room: str
    visited_rooms: List[str] = []
    defeated_enemies: List[str] = []
    collected_treasures: List[str] = []
    completed: bool = False

class StartMissionRequest(BaseModel):
    character_name: str
    mission_id: str

class MissionActionRequest(BaseModel):
    character_name: str
    mission_id: str
    action: str  # "move", "fight", "collect"
    target: Optional[str] = None

class MissionActionResponse(BaseModel):
    success: bool
    message: str
    current_room: Dict
    character_status: Dict
    mission_progress: Dict
