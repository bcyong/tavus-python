#!/usr/bin/env python3

from typing import Optional
from datetime import datetime

class Replica:
  """Represents a Tavus Replica object"""
  
  def __init__(self, replica_id: str, replica_name: str, replica_type: str, 
               status: str, training_progress: str, 
               created_at: str, updated_at: str,
               thumbnail_video_url: Optional[str] = None):
    self.replica_id = replica_id
    self.replica_name = replica_name
    self.replica_type = replica_type
    self.status = status
    self.training_progress = training_progress
    self.created_at = created_at
    self.updated_at = updated_at
    self.thumbnail_video_url = thumbnail_video_url
  
  @classmethod
  def from_dict(cls, data: dict) -> 'Replica':
    """Create a Replica instance from a dictionary (API response)"""
    return cls(
      replica_id=data.get('replica_id', ''),
      replica_name=data.get('replica_name', ''),
      replica_type=data.get('replica_type', ''),
      status=data.get('status', ''),
      training_progress=data.get('training_progress', ''),
      created_at=data.get('created_at', ''),
      updated_at=data.get('updated_at', ''),
      thumbnail_video_url=data.get('thumbnail_video_url')
    )
  
  def to_dict(self) -> dict:
    """Convert the Replica instance to a dictionary"""
    return {
      'replica_id': self.replica_id,
      'replica_name': self.replica_name,
      'replica_type': self.replica_type,
      'status': self.status,
      'training_progress': self.training_progress,
      'created_at': self.created_at,
      'updated_at': self.updated_at,
      'thumbnail_video_url': self.thumbnail_video_url
    }
  
  def is_completed(self) -> bool:
    """Check if the replica training is completed"""
    return self.status == 'completed'
  
  def is_training(self) -> bool:
    """Check if the replica is currently training"""
    return self.status == 'training'
  
  def get_training_percentage(self) -> int:
    """Extract training percentage from training_progress string (e.g., '100/100' -> 100)"""
    try:
      if '/' in self.training_progress:
        current, total = self.training_progress.split('/')
        return int((int(current) / int(total)) * 100)
      return 0
    except (ValueError, AttributeError):
      return 0
  
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
    """Return a short one-line representation of the replica"""
    status_emoji = "✅" if self.is_completed() else "🔄" if self.is_training() else "❌"
    return f"{status_emoji} {self.replica_name} ({self.replica_id}) - {self.status} - {self.training_progress}"
  
  def display_verbose(self) -> str:
    """Return a verbose multi-line representation of the replica"""
    lines = [
      f"Replica Details:",
      f"  ID: {self.replica_id}",
      f"  Name: {self.replica_name}",
      f"  Type: {self.replica_type}",
      f"  Status: {self.status}",
      f"  Training Progress: {self.training_progress}",
      f"  Created: {self.created_at}",
    ]
    
    if self.thumbnail_video_url:
      lines.append(f"  Thumbnail URL: {self.thumbnail_video_url}")
    
    # Add computed properties
    created_date = self.get_created_date()
    if created_date:
      lines.append(f"  Created Date: {created_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    updated_date = self.get_updated_date()
    if updated_date:
      lines.append(f"  Updated Date: {updated_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    training_pct = self.get_training_percentage()
    lines.append(f"  Training Percentage: {training_pct}%")
    
    return "\n".join(lines)
  
  def print_short(self):
    """Print a short one-line representation of the replica"""
    print(self.display_short())
  
  def print_verbose(self):
    """Print a verbose multi-line representation of the replica"""
    print(self.display_verbose())
  
  def __str__(self) -> str:
    """String representation of the Replica"""
    return f"Replica(id={self.replica_id}, name='{self.replica_name}', type='{self.replica_type}', status='{self.status}')"
  
  def __repr__(self) -> str:
    """Detailed string representation of the Replica"""
    return f"Replica(replica_id='{self.replica_id}', replica_name='{self.replica_name}', replica_type='{self.replica_type}', status='{self.status}', training_progress='{self.training_progress}', created_at='{self.created_at}')"
  
  def __eq__(self, other) -> bool:
    """Check if two Replica instances are equal"""
    if not isinstance(other, Replica):
      return False
    return self.replica_id == other.replica_id
  
  def __hash__(self) -> int:
    """Hash based on replica_id"""
    return hash(self.replica_id) 