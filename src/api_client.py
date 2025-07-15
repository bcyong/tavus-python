#!/usr/bin/env python3

import requests
from typing import Tuple, List, Dict, Optional
from models import Replica, Persona, Video, Conversation

class TavusAPIClient:
  """Client for interacting with the Tavus API"""
  
  def __init__(self, api_key: str):
    self.api_key = api_key
    self.base_url = "https://tavusapi.com/v2"
    self.headers = {"x-api-key": api_key}
  
  def list_replicas(self, limit: int = 1000) -> Tuple[bool, str, List[Replica]]:
    """
    List replicas from Tavus API
    
    Args:
      limit: The number of replicas to return. Default is 1000.
      
    Returns:
      Tuple[bool, str, List[Replica]]: (success, message, replicas_list)
    """
    url = f"{self.base_url}/replicas?verbose=true&limit={limit}"
    
    try:
      response = requests.request("GET", url, headers=self.headers)
      
      if response.status_code == 200:
        response_data = response.json()
        replicas_data = response_data.get('data', [])
        replicas = [Replica.from_dict(replica_data) for replica_data in replicas_data]
        return True, f"Successfully fetched {len(replicas)} replica(s)", replicas
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}", []
        
    except Exception as e:
      return False, f"Error fetching replicas: {e}", []
  
  def get_replica(self, replica_id: str) -> Tuple[bool, str, Optional[Replica]]:
    """
    Get a specific replica by ID
    
    Args:
      replica_id: The ID of the replica to fetch
      
    Returns:
      Tuple[bool, str, Optional[Replica]]: (success, message, replica_data)
    """
    url = f"{self.base_url}/replicas/{replica_id}?verbose=true"
    
    try:
      response = requests.request("GET", url, headers=self.headers)
      
      if response.status_code == 200:
        replica_data = response.json()
        replica = Replica.from_dict(replica_data)
        return True, "Successfully fetched replica", replica
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}", None
        
    except Exception as e:
      return False, f"Error fetching replica: {e}", None
  
  def create_replica(self, replica_data: Dict) -> Tuple[bool, str, Optional[Dict]]:
    """
    Create a new replica
    
    Args:
      replica_data: Dictionary containing replica creation parameters
      
    Returns:
      Tuple[bool, str, Optional[Dict]]: (success, message, response_data)
    """
    url = f"{self.base_url}/replicas"
    
    try:
      response = requests.request("POST", url, headers=self.headers, json=replica_data)
      
      if response.status_code == 200:
        response_data = response.json()
        return True, "Successfully created replica", response_data
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}", None
        
    except Exception as e:
      return False, f"Error creating replica: {e}", None
  
  def delete_replica(self, replica_id: str) -> Tuple[bool, str]:
    """
    Delete a replica by ID
    
    Args:
      replica_id: The ID of the replica to delete
      
    Returns:
      Tuple[bool, str]: (success, message)
    """
    url = f"{self.base_url}/replicas/{replica_id}"
    
    try:
      response = requests.request("DELETE", url, headers=self.headers)
      
      if response.status_code == 204:
        return True, "Successfully deleted replica"
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}"
        
    except Exception as e:
      return False, f"Error deleting replica: {e}"
  
  def rename_replica(self, replica_id: str, new_name: str) -> Tuple[bool, str]:
    """
    Rename a replica
    
    Args:
      replica_id: The ID of the replica to rename
      new_name: The new name for the replica
      
    Returns:
      Tuple[bool, str]: (success, message)
    """
    url = f"{self.base_url}/replicas/{replica_id}/name"
    payload = {"replica_name": new_name}
    
    try:
      response = requests.request("PATCH", url, headers=self.headers, json=payload)
      
      if response.status_code == 204:
        return True, "Successfully renamed replica"
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}"
        
    except Exception as e:
      return False, f"Error renaming replica: {e}"
  
  def list_personas(self, persona_type: str = "system", limit: int = 1000) -> Tuple[bool, str, List[Persona]]:
    """
    Fetch personas from Tavus API
    
    Args:
      persona_type: Filter personas by type. Options: "user", "system". Defaults to "system".
      
    Returns:
      Tuple[bool, str, List[Persona]]: (success, message, personas_list)
    """
    url = f"{self.base_url}/personas?limit={limit}&persona_type={persona_type}"
    
    try:
      response = requests.request("GET", url, headers=self.headers)
      
      if response.status_code == 200:
        response_data = response.json()
        personas_data = response_data.get('data', [])
        personas = [Persona.from_dict(persona_data) for persona_data in personas_data]
        return True, f"Successfully fetched {len(personas)} persona(s)", personas
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}", []
        
    except Exception as e:
      return False, f"Error fetching personas: {e}", []
  
  def create_persona(self, persona_data: Dict) -> Tuple[bool, str, Optional[Persona]]:
    """
    Create a new persona
    
    Args:
      persona_data: Dictionary containing persona creation parameters
      
    Returns:
      Tuple[bool, str, Optional[Persona]]: (success, message, created_persona_data)
    """
    url = f"{self.base_url}/personas"
    
    try:
      response = requests.request("POST", url, headers=self.headers, json=persona_data)
      
      if response.status_code == 200:
        created_persona_data = response.json()
        persona = Persona.from_dict(created_persona_data)
        return True, "Successfully created persona", persona
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}", None
        
    except Exception as e:
      return False, f"Error creating persona: {e}", None
  
  def delete_persona(self, persona_id: str) -> Tuple[bool, str]:
    """
    Delete a persona by ID
    
    Args:
      persona_id: The ID of the persona to delete
      
    Returns:
      Tuple[bool, str]: (success, message)
    """
    url = f"{self.base_url}/personas/{persona_id}"
    
    try:
      response = requests.request("DELETE", url, headers=self.headers)
      
      if response.status_code == 204:
        return True, "Successfully deleted persona"
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}"
        
    except Exception as e:
      return False, f"Error deleting persona: {e}"
  
  def patch_persona(self, persona_id: str, patch_data: Dict) -> Tuple[bool, str]:
    """
    Update a persona with PATCH request
    
    Args:
      persona_id: The ID of the persona to update
      patch_data: Dictionary containing the fields to update
      
    Returns:
      Tuple[bool, str]: (success, message)
    """
    url = f"{self.base_url}/personas/{persona_id}"
    
    try:
      response = requests.request("PATCH", url, headers=self.headers, json=patch_data)
      
      if response.status_code == 200:
        return True, "Successfully updated persona"
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}"
        
    except Exception as e:
      return False, f"Error updating persona: {e}"
  
  def generate_video(self, video_data: Dict) -> Tuple[bool, str, Optional[Video]]:
    """
    Generate a new video
    
    Args:
      video_data: Dictionary containing video generation parameters
      
    Returns:
      Tuple[bool, str, Optional[Video]]: (success, message, generated_video_data)
    """
    url = f"{self.base_url}/videos"
    
    try:
      response = requests.request("POST", url, headers=self.headers, json=video_data)
      
      if response.status_code == 200:
        generated_video_data = response.json()
        video = Video.from_dict(generated_video_data)
        return True, "Successfully generated video", video
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}", None
        
    except Exception as e:
      return False, f"Error generating video: {e}", None

  def get_video(self, video_id: str) -> Tuple[bool, str, Optional[Video]]:
    """
    Get a specific video by ID
    
    Args:
      video_id: The ID of the video to fetch
      
    Returns:
      Tuple[bool, str, Optional[Video]]: (success, message, video_data)
    """
    url = f"{self.base_url}/videos/{video_id}"
    
    try:
      response = requests.request("GET", url, headers=self.headers)
      
      if response.status_code == 200:
        video_data = response.json()
        video = Video.from_dict(video_data)
        return True, "Successfully fetched video", video
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}", None
        
    except Exception as e:
      return False, f"Error fetching video: {e}", None

  def list_videos(self, limit: int = 1000) -> Tuple[bool, str, List[Video]]:
    """
    List videos from Tavus API
    
    Args:
      limit: The number of videos to return. Default is 1000.
      
    Returns:
      Tuple[bool, str, List[Video]]: (success, message, videos_list)
    """
    url = f"{self.base_url}/videos?limit={limit}"
    
    try:
      response = requests.request("GET", url, headers=self.headers)
      
      if response.status_code == 200:
        response_data = response.json()
        videos_data = response_data.get('data', [])
        videos = [Video.from_dict(video_data) for video_data in videos_data]
        return True, f"Successfully fetched {len(videos)} video(s)", videos
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}", []
        
    except Exception as e:
      return False, f"Error fetching videos: {e}", []

  def delete_video(self, video_id: str) -> Tuple[bool, str]:
    """
    Delete a video by ID
    
    Args:
      video_id: The ID of the video to delete
      
    Returns:
      Tuple[bool, str]: (success, message)
    """
    url = f"{self.base_url}/videos/{video_id}"
    
    try:
      response = requests.request("DELETE", url, headers=self.headers)
      
      if response.status_code == 204:
        return True, "Successfully deleted video"
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}"
        
    except Exception as e:
      return False, f"Error deleting video: {e}"

  def rename_video(self, video_id: str, new_name: str) -> Tuple[bool, str]:
    """
    Rename a video
    
    Args:
      video_id: The ID of the video to rename
      new_name: The new name for the video
      
    Returns:
      Tuple[bool, str]: (success, message)
    """
    url = f"{self.base_url}/videos/{video_id}/name"
    payload = {"video_name": new_name}
    
    try:
      response = requests.request("PATCH", url, headers=self.headers, json=payload)
      
      if response.status_code == 204:
        return True, "Successfully renamed video"
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}"
        
    except Exception as e:
      return False, f"Error renaming video: {e}"

  def list_conversations(self, limit: int = 1000, status: Optional[str] = None) -> Tuple[bool, str, List[Conversation]]:
    """
    List conversations from Tavus API
    
    Args:
      limit: The number of conversations to return. Default is 1000.
      status: Optional status filter for conversations (e.g., 'active', 'completed', etc.)
      
    Returns:
      Tuple[bool, str, List[Conversation]]: (success, message, conversations_list)
    """
    url = f"{self.base_url}/conversations?limit={limit}"
    if status:
      url += f"&status={status}"
    
    try:
      response = requests.request("GET", url, headers=self.headers)
      
      if response.status_code == 200:
        response_data = response.json()
        conversations_data = response_data.get('data', [])
        conversations = [Conversation.from_dict(conv_data) for conv_data in conversations_data]
        return True, f"Successfully fetched {len(conversations)} conversation(s)", conversations
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}", []
        
    except Exception as e:
      return False, f"Error fetching conversations: {e}", []

  def get_conversation(self, conversation_id: str) -> Tuple[bool, str, Optional[Conversation]]:
    """
    Get a specific conversation by ID
    
    Args:
      conversation_id: The ID of the conversation to fetch
      
    Returns:
      Tuple[bool, str, Optional[Conversation]]: (success, message, conversation_data)
    """
    url = f"{self.base_url}/conversations/{conversation_id}?verbose=true"
    
    try:
      response = requests.request("GET", url, headers=self.headers)
      
      if response.status_code == 200:
        conversation_data = response.json()
        conversation = Conversation.from_dict(conversation_data)
        return True, "Successfully fetched conversation", conversation
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}", None
        
    except Exception as e:
      return False, f"Error fetching conversation: {e}", None

  def create_conversation(self, conversation_data: Dict) -> Tuple[bool, str, Optional[Conversation]]:
    """
    Create a new conversation
    
    Args:
      conversation_data: Dictionary containing conversation creation parameters
        Required fields: persona_id, replica_id
        Optional fields: conversation_name, metadata
      
    Returns:
      Tuple[bool, str, Optional[Conversation]]: (success, message, created_conversation)
    """
    url = f"{self.base_url}/conversations"
    
    try:
      response = requests.request("POST", url, headers=self.headers, json=conversation_data)
      
      if response.status_code == 200:
        created_conversation_data = response.json()
        conversation = Conversation.from_dict(created_conversation_data)
        return True, "Successfully created conversation", conversation
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}", None
        
    except Exception as e:
      return False, f"Error creating conversation: {e}", None

  def delete_conversation(self, conversation_id: str) -> Tuple[bool, str]:
    """
    Delete a conversation by ID
    
    Args:
      conversation_id: The ID of the conversation to delete
      
    Returns:
      Tuple[bool, str]: (success, message)
    """
    url = f"{self.base_url}/conversations/{conversation_id}"
    
    try:
      response = requests.request("DELETE", url, headers=self.headers)
      
      if response.status_code == 204:
        return True, "Successfully deleted conversation"
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}"
        
    except Exception as e:
      return False, f"Error deleting conversation: {e}"

  def end_conversation(self, conversation_id: str) -> Tuple[bool, str]:
    """
    End a conversation by ID
    
    Args:
      conversation_id: The ID of the conversation to end
      
    Returns:
      Tuple[bool, str]: (success, message)
    """
    url = f"{self.base_url}/conversations/{conversation_id}/end"
    
    try:
      response = requests.request("POST", url, headers=self.headers)
      
      if response.status_code == 200:
        return True, "Successfully ended conversation"
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}"
        
    except Exception as e:
      return False, f"Error ending conversation: {e}"

