#!/usr/bin/env python3

from typing import Optional, Dict, Any
from datetime import datetime

class Video:
  """Represents a Tavus Video object"""
  
  def __init__(self, video_id: str, video_name: str, status: str, created_at: str,
               data: Optional[Dict[str, Any]] = None, download_url: Optional[str] = None,
               stream_url: Optional[str] = None, hosted_url: Optional[str] = None,
               status_details: Optional[str] = None, updated_at: Optional[str] = None,
               still_image_thumbnail_url: Optional[str] = None, gif_thumbnail_url: Optional[str] = None):
    self.video_id = video_id
    self.video_name = video_name
    self.status = status
    self.created_at = created_at
    self.data = data or {}
    self.download_url = download_url
    self.stream_url = stream_url
    self.hosted_url = hosted_url
    self.status_details = status_details
    self.updated_at = updated_at
    self.still_image_thumbnail_url = still_image_thumbnail_url
    self.gif_thumbnail_url = gif_thumbnail_url
  
  @classmethod
  def from_dict(cls, data: dict) -> 'Video':
    """Create a Video instance from a dictionary (API response)"""
    return cls(
      video_id=data.get('video_id', ''),
      video_name=data.get('video_name', ''),
      status=data.get('status', ''),
      created_at=data.get('created_at', ''),
      data=data.get('data', {}),
      download_url=data.get('download_url'),
      stream_url=data.get('stream_url'),
      hosted_url=data.get('hosted_url'),
      status_details=data.get('status_details'),
      updated_at=data.get('updated_at'),
      still_image_thumbnail_url=data.get('still_image_thumbnail_url'),
      gif_thumbnail_url=data.get('gif_thumbnail_url')
    )
  
  def to_dict(self) -> dict:
    """Convert the Video instance to a dictionary"""
    return {
      'video_id': self.video_id,
      'video_name': self.video_name,
      'status': self.status,
      'created_at': self.created_at,
      'data': self.data,
      'download_url': self.download_url,
      'stream_url': self.stream_url,
      'hosted_url': self.hosted_url,
      'status_details': self.status_details,
      'updated_at': self.updated_at,
      'still_image_thumbnail_url': self.still_image_thumbnail_url,
      'gif_thumbnail_url': self.gif_thumbnail_url
    }
  
  def is_completed(self) -> bool:
    """Check if the video generation is completed"""
    return self.status in ['ready']
  
  def is_processing(self) -> bool:
    """Check if the video is currently being processed"""
    return self.status in ['generating']
  
  def is_failed(self) -> bool:
    """Check if the video generation failed"""
    return self.status in ['error']
  
  def is_pending(self) -> bool:
    """Check if the video is pending generation"""
    return self.status in ['queued']
  
  def has_script(self) -> bool:
    """Check if the video has a script in the data"""
    return bool(self.data.get('script'))
  
  def has_download_url(self) -> bool:
    """Check if the video has a downloadable URL"""
    return bool(self.download_url and self.download_url.strip())
  
  def has_stream_url(self) -> bool:
    """Check if the video has a stream URL"""
    return bool(self.stream_url and self.stream_url.strip())
  
  def has_hosted_url(self) -> bool:
    """Check if the video has a hosted URL"""
    return bool(self.hosted_url and self.hosted_url.strip())
  
  def has_still_thumbnail(self) -> bool:
    """Check if the video has a still image thumbnail URL"""
    return bool(self.still_image_thumbnail_url and self.still_image_thumbnail_url.strip())
  
  def has_gif_thumbnail(self) -> bool:
    """Check if the video has a GIF thumbnail URL"""
    return bool(self.gif_thumbnail_url and self.gif_thumbnail_url.strip())
  
  def get_script(self) -> Optional[str]:
    """Get the script from the data dictionary"""
    return self.data.get('script')
  
  def get_script_preview(self, max_length: int = 100) -> str:
    """Get a preview of the script"""
    script = self.get_script()
    if not script:
      return "No script"
    
    if len(script) <= max_length:
      return script
    
    return script[:max_length] + "..."
  
  def display_short(self) -> str:
    """Return a short one-line representation of the video"""
    status_emoji = "✅" if self.is_completed() else "🔄" if self.is_processing() else "❌" if self.is_failed() else "⏳"
    return f"{status_emoji} {self.video_name} ({self.video_id}) - {self.status}"
  
  def display_verbose(self) -> str:
    """Return a verbose multi-line representation of the video"""
    lines = [
      f"Video Details:",
      f"  ID: {self.video_id}",
      f"  Name: {self.video_name}",
      f"  Status: {self.status}",
      f"  Created: {self.created_at}",
      f"  Updated: {self.updated_at}",
    ]
    if self.status_details:
      lines.append(f"  Status Details: {self.status_details}")
    
    if self.download_url:
      lines.append(f"  Download URL: {self.download_url}")
    
    if self.stream_url:
      lines.append(f"  Stream URL: {self.stream_url}")
    
    if self.hosted_url:
      lines.append(f"  Hosted URL: {self.hosted_url}")
    
    if self.still_image_thumbnail_url:
      lines.append(f"  Still Image Thumbnail: {self.still_image_thumbnail_url}")
    
    if self.gif_thumbnail_url:
      lines.append(f"  GIF Thumbnail: {self.gif_thumbnail_url}")
    
    # Add data information
    if self.data:
      lines.append(f"  Data: {len(self.data)} items")
      for key, value in self.data.items():
        if key == 'script':
          lines.append(f"    - Script: {self.get_script_preview(10000)}")
        else:
          lines.append(f"    - {key}: {value}")
    else:
      lines.append(f"  Data: None")
    
    return "\n".join(lines)
  
  def print_short(self):
    """Print a short one-line representation of the video"""
    print(self.display_short())
  
  def print_verbose(self):
    """Print a verbose multi-line representation of the video"""
    print(self.display_verbose())
  
  def __str__(self) -> str:
    """String representation of the Video"""
    return f"Video(id={self.video_id}, name='{self.video_name}', status='{self.status}')"
  
  def __repr__(self) -> str:
    """Detailed string representation of the Video"""
    return f"Video(video_id='{self.video_id}', video_name='{self.video_name}', status='{self.status}', created_at='{self.created_at}')"
  
  def __eq__(self, other) -> bool:
    """Check if two Video instances are equal"""
    if not isinstance(other, Video):
      return False
    return self.video_id == other.video_id
  
  def __hash__(self) -> int:
    """Hash based on video_id"""
    return hash(self.video_id) 