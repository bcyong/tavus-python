#!/usr/bin/env python3

from typing import Dict, List, Optional, Any
from datetime import datetime

class Conversation:
  """Represents a Tavus Conversation object"""
  
  def __init__(self, conversation_id: str, conversation_name: str, conversation_url: str,
               callback_url: Optional[str] = None, status: str = "", replica_id: str = "",
               persona_id: str = "", created_at: str = "", updated_at: str = ""):
    self.conversation_id = conversation_id
    self.conversation_name = conversation_name
    self.conversation_url = conversation_url
    self.callback_url = callback_url
    self.status = status
    self.replica_id = replica_id
    self.persona_id = persona_id
    self.created_at = created_at
    self.updated_at = updated_at
  
  @classmethod
  def from_dict(cls, data: Dict[str, Any]) -> 'Conversation':
    """Create a Conversation instance from a dictionary (API response)"""
    return cls(
      conversation_id=data.get('conversation_id', ''),
      conversation_name=data.get('conversation_name', ''),
      conversation_url=data.get('conversation_url', ''),
      callback_url=data.get('callback_url'),
      status=data.get('status', ''),
      replica_id=data.get('replica_id', ''),
      persona_id=data.get('persona_id', ''),
      created_at=data.get('created_at', ''),
      updated_at=data.get('updated_at', '')
    )
  
  def to_dict(self) -> Dict[str, Any]:
    """Convert the Conversation instance to a dictionary"""
    result = {
      'conversation_id': self.conversation_id,
      'conversation_name': self.conversation_name,
      'conversation_url': self.conversation_url,
      'status': self.status,
      'replica_id': self.replica_id,
      'persona_id': self.persona_id,
      'created_at': self.created_at,
      'updated_at': self.updated_at
    }
    
    if self.callback_url:
      result['callback_url'] = self.callback_url
      
    return result
  
  def get_created_date(self) -> Optional[datetime]:
    """Parse and return the created_at date as a datetime object"""
    try:
      return datetime.fromisoformat(self.created_at.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
      return None
  
  def get_updated_date(self) -> Optional[datetime]:
    """Parse and return the updated_at date as a datetime object"""
    try:
      return datetime.fromisoformat(self.updated_at.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
      return None
  
  def display_short(self) -> str:
    """Return a short one-line representation of the conversation"""
    return f"{self.conversation_name} ({self.conversation_id}) - {self.status}"
  
  def display_verbose(self) -> str:
    """Return a verbose multi-line representation of the conversation"""
    lines = [
      f"Conversation Details:",
      f"  ID: {self.conversation_id}",
      f"  Name: {self.conversation_name}",
      f"  URL: {self.conversation_url}",
      f"  Status: {self.status}",
      f"  Replica ID: {self.replica_id}",
      f"  Persona ID: {self.persona_id}",
      f"  Created: {self.created_at}",
      f"  Updated: {self.updated_at}"
    ]
    
    if self.callback_url:
      lines.append(f"  Callback URL: {self.callback_url}")
    
    return "\n".join(lines)
  
  def print_short(self):
    """Print a short one-line representation of the conversation"""
    print(self.display_short())
  
  def print_verbose(self):
    """Print a verbose multi-line representation of the conversation"""
    print(self.display_verbose())
  
  def __str__(self) -> str:
    """String representation of the Conversation"""
    return self.display_short()
  
  def __repr__(self) -> str:
    """Detailed string representation of the Conversation"""
    return f"Conversation(conversation_id='{self.conversation_id}', conversation_name='{self.conversation_name}', status='{self.status}')"
  
  def __eq__(self, other) -> bool:
    """Check if two Conversation instances are equal"""
    if not isinstance(other, Conversation):
      return False
    return self.conversation_id == other.conversation_id
  
  def __hash__(self) -> int:
    """Hash based on conversation_id"""
    return hash(self.conversation_id) 