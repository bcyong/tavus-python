#!/usr/bin/env python3

import requests
from typing import Tuple, List, Dict, Optional

class TavusAPIClient:
  """Client for interacting with the Tavus API"""
  
  def __init__(self, api_key: str):
    self.api_key = api_key
    self.base_url = "https://tavusapi.com/v2"
    self.headers = {"x-api-key": api_key}
  
  def fetch_replicas(self) -> Tuple[bool, str, List[Dict]]:
    """
    Fetch replicas from Tavus API
    
    Returns:
      Tuple[bool, str, List[Dict]]: (success, message, replicas_list)
    """
    url = f"{self.base_url}/replicas?verbose=true"
    
    try:
      response = requests.request("GET", url, headers=self.headers)
      
      if response.status_code == 200:
        response_data = response.json()
        replicas = response_data.get('data', [])
        return True, f"Successfully fetched {len(replicas)} replica(s)", replicas
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}", []
        
    except Exception as e:
      return False, f"Error fetching replicas: {e}", []
  
  def get_replica(self, replica_id: str) -> Tuple[bool, str, Optional[Dict]]:
    """
    Get a specific replica by ID
    
    Args:
      replica_id: The ID of the replica to fetch
      
    Returns:
      Tuple[bool, str, Optional[Dict]]: (success, message, replica_data)
    """
    url = f"{self.base_url}/replicas/{replica_id}?verbose=true"
    
    try:
      response = requests.request("GET", url, headers=self.headers)
      
      if response.status_code == 200:
        replica_data = response.json()
        return True, "Successfully fetched replica", replica_data
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
      Tuple[bool, str, Optional[Dict]]: (success, message, created_replica_data)
    """
    url = f"{self.base_url}/replicas"
    
    try:
      response = requests.request("POST", url, headers=self.headers, json=replica_data)
      
      if response.status_code == 201:
        created_replica = response.json()
        return True, "Successfully created replica", created_replica
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
    url = f"{self.base_url}/replicas/{replica_id}"
    payload = {"replica_name": new_name}
    
    try:
      response = requests.request("PATCH", url, headers=self.headers, json=payload)
      
      if response.status_code == 200:
        return True, "Successfully renamed replica"
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}"
        
    except Exception as e:
      return False, f"Error renaming replica: {e}"
  
  def fetch_personas(self) -> Tuple[bool, str, List[Dict]]:
    """
    Fetch personas from Tavus API
    
    Returns:
      Tuple[bool, str, List[Dict]]: (success, message, personas_list)
    """
    url = f"{self.base_url}/personas"
    
    try:
      response = requests.request("GET", url, headers=self.headers)
      
      if response.status_code == 200:
        response_data = response.json()
        personas = response_data.get('data', [])
        return True, f"Successfully fetched {len(personas)} persona(s)", personas
      else:
        return False, f"Error: HTTP {response.status_code} - {response.text}", []
        
    except Exception as e:
      return False, f"Error fetching personas: {e}", []
  
  def create_persona(self, persona_data: Dict) -> Tuple[bool, str, Optional[Dict]]:
    """
    Create a new persona
    
    Args:
      persona_data: Dictionary containing persona creation parameters
      
    Returns:
      Tuple[bool, str, Optional[Dict]]: (success, message, created_persona_data)
    """
    url = f"{self.base_url}/personas"
    
    try:
      response = requests.request("POST", url, headers=self.headers, json=persona_data)
      
      if response.status_code == 201:
        created_persona = response.json()
        return True, "Successfully created persona", created_persona
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