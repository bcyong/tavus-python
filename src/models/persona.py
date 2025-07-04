#!/usr/bin/env python3

from typing import Optional, Dict, Any
from datetime import datetime

class Persona:
  """Represents a Tavus Persona object"""
  
  def __init__(self, persona_id: str, persona_name: str, default_replica_id: str,
               created_at: str, updated_at: str, system_prompt: Optional[str] = None,
               context: Optional[str] = None, layers: Optional[Dict[str, Any]] = None):
    self.persona_id = persona_id
    self.persona_name = persona_name
    self.default_replica_id = default_replica_id
    self.created_at = created_at
    self.updated_at = updated_at
    self.system_prompt = system_prompt
    self.context = context
    self.layers = layers or {}
  
  @classmethod
  def from_dict(cls, data: dict) -> 'Persona':
    """Create a Persona instance from a dictionary (API response)"""
    return cls(
      persona_id=data.get('persona_id', ''),
      persona_name=data.get('persona_name', ''),
      default_replica_id=data.get('default_replica_id', ''),
      created_at=data.get('created_at', ''),
      updated_at=data.get('updated_at', ''),
      system_prompt=data.get('system_prompt'),
      context=data.get('context'),
      layers=data.get('layers', {})
    )
  
  def to_dict(self) -> dict:
    """Convert the Persona instance to a dictionary"""
    return {
      'persona_id': self.persona_id,
      'persona_name': self.persona_name,
      'default_replica_id': self.default_replica_id,
      'created_at': self.created_at,
      'updated_at': self.updated_at,
      'system_prompt': self.system_prompt,
      'context': self.context,
      'layers': self.layers
    }
  
  def has_default_replica(self) -> bool:
    """Check if the persona has a default replica assigned"""
    return bool(self.default_replica_id and self.default_replica_id.strip())
  
  def get_llm_config(self) -> Optional[Dict[str, Any]]:
    """Get the LLM configuration from layers"""
    return self.layers.get('llm')
  
  def get_tts_config(self) -> Optional[Dict[str, Any]]:
    """Get the TTS configuration from layers"""
    return self.layers.get('tts')
  
  def get_stt_config(self) -> Optional[Dict[str, Any]]:
    """Get the STT configuration from layers"""
    return self.layers.get('stt')
  
  def get_perception_config(self) -> Optional[Dict[str, Any]]:
    """Get the perception configuration from layers"""
    return self.layers.get('perception')
  
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
  
  def get_system_prompt_preview(self, max_length: int = 100) -> str:
    """Get a preview of the system prompt"""
    if not self.system_prompt:
      return "No system prompt"
    
    if len(self.system_prompt) <= max_length:
      return self.system_prompt
    
    return self.system_prompt[:max_length] + "..."
  
  def get_context_preview(self, max_length: int = 100) -> str:
    """Get a preview of the context"""
    if not self.context:
      return "No context"
    
    if len(self.context) <= max_length:
      return self.context
    
    return self.context[:max_length] + "..."
  
  def display_short(self) -> str:
    """Return a short one-line representation of the persona"""
    replica_indicator = "🔗" if self.has_default_replica() else "🔴"
    return f"{replica_indicator} {self.persona_name} ({self.persona_id}) - Default Replica: {self.default_replica_id or 'None'}"
  
  def display_verbose(self) -> str:
    """Return a verbose multi-line representation of the persona"""
    lines = [
      f"Persona Details:",
      f"  ID: {self.persona_id}",
      f"  Name: {self.persona_name}",
      f"  Default Replica ID: {self.default_replica_id or 'None'}",
    ]
    
    # Add computed properties
    created_date = self.get_created_date()
    if created_date:
      lines.append(f"  Created Date: {created_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    updated_date = self.get_updated_date()
    if updated_date:
      lines.append(f"  Updated Date: {updated_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Add system prompt preview
    lines.append(f"  System Prompt: {self.get_system_prompt_preview(1000)}")
    
    # Add context preview
    lines.append(f"  Context: {self.get_context_preview(1000)}")
    
    # Add layer information with full data
    if self.layers:
      lines.append(f"  Layers: {len(self.layers)} configured")
      for layer_name, layer_data in self.layers.items():
        lines.append(f"    - {layer_name}:")
        if isinstance(layer_data, dict):
          for key, value in layer_data.items():
            lines.append(f"      {key}: {value}")
        else:
          lines.append(f"      {layer_data}")
    else:
      lines.append(f"  Layers: None configured")
    
    return "\n".join(lines)
  
  def print_short(self):
    """Print a short one-line representation of the persona"""
    print(self.display_short())
  
  def print_verbose(self):
    """Print a verbose multi-line representation of the persona"""
    print(self.display_verbose())
  
  def __str__(self) -> str:
    """String representation of the Persona"""
    return f"Persona(id={self.persona_id}, name='{self.persona_name}', default_replica='{self.default_replica_id}')"
  
  def __repr__(self) -> str:
    """Detailed string representation of the Persona"""
    return f"Persona(persona_id='{self.persona_id}', persona_name='{self.persona_name}', default_replica_id='{self.default_replica_id}', created_at='{self.created_at}', updated_at='{self.updated_at}')"
  
  def __eq__(self, other) -> bool:
    """Check if two Persona instances are equal"""
    if not isinstance(other, Persona):
      return False
    return self.persona_id == other.persona_id
  
  def __hash__(self) -> int:
    """Hash based on persona_id"""
    return hash(self.persona_id) 