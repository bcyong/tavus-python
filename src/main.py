#!/usr/bin/env python3

from timeit import Timer
from bullet import Input, Bullet, YesNo
import sys
import os
from enum import Enum
from api_client import TavusAPIClient
from yaspin import yaspin
import time

# State enum
class State(Enum):
  MAIN_MENU = "main_menu"
  SET_API_KEY = "set_api_key"
  WORK_WITH_REPLICAS = "work_with_replicas"
  WORK_WITH_PERSONAS = "work_with_personas"
  CREATE_REPLICA = "create_replica"
  LIST_REPLICAS = "list_replicas"
  MODIFY_REPLICA = "modify_replica"
  DELETE_REPLICA = "delete_replica"
  CREATE_PERSONA = "create_persona"
  LIST_PERSONAS = "list_personas"
  DELETE_PERSONA = "delete_persona"
  EXIT = "exit"

# Global variables
api_client = None  # Global API client instance
api_key = None
current_state = State.MAIN_MENU
replicas = []  # Global list to store replicas
personas = []  # Global list to store personas

def main():
  print("Welcome to the Tavus Python CLI Tool!")

  set_initial_api_key()

  print("Updating replicas and personas...")
  with yaspin(text="Loading replicas..."):
    update_replicas()
  with yaspin(text="Loading personas..."):
    update_personas()
  print("Initialization complete!")

  # State machine loop
  while current_state != State.EXIT:
    execute_current_state()

def execute_current_state():
  """Execute the current state and update the next state"""
  global current_state
  
  if current_state == State.MAIN_MENU:
    current_state = execute_main_menu()
  elif current_state == State.SET_API_KEY:
    current_state = execute_set_api_key()
  elif current_state == State.WORK_WITH_REPLICAS:
    current_state = execute_work_with_replicas()
  elif current_state == State.WORK_WITH_PERSONAS:
    current_state = execute_work_with_personas()
  elif current_state == State.CREATE_REPLICA:
    current_state = execute_create_replica()
  elif current_state == State.LIST_REPLICAS:
    current_state = execute_list_replicas()
  elif current_state == State.MODIFY_REPLICA:
    current_state = execute_modify_replica()
  elif current_state == State.DELETE_REPLICA:
    current_state = execute_delete_replica()
  elif current_state == State.CREATE_PERSONA:
    current_state = execute_create_persona()
  elif current_state == State.LIST_PERSONAS:
    current_state = execute_list_personas()
  elif current_state == State.DELETE_PERSONA:
    current_state = execute_delete_persona()
  else:
    print(f"Unknown state: {current_state}")
    current_state = State.MAIN_MENU

def execute_main_menu():
  """Execute main menu and return next state"""
  print("\n=== Main Menu ===")
  print(f"Tavus API key: {api_key}")
  
  cli = Bullet(
    prompt="What would you like to do?",
    choices=["Set API Key", "Work with Replicas", "Work with Personas", "Exit"],
    bullet="🧑",
    margin=2,
    shift=0,
  )
  result = cli.launch()

  if result == "Set API Key":
    return State.SET_API_KEY
  elif result == "Work with Replicas":
    return State.WORK_WITH_REPLICAS
  elif result == "Work with Personas":
    return State.WORK_WITH_PERSONAS
  elif result == "Exit":
    return State.EXIT
  else:
    return State.MAIN_MENU

def set_initial_api_key():
  """Set the initial API key from .tavus_api_key file"""
  global api_key, api_client
  
  if os.path.exists(".tavus_api_key"):
    with open(".tavus_api_key", "r") as file:
      api_key = file.read().strip()
      api_client = TavusAPIClient(api_key)
  else:
    cli = Input(prompt="Enter your Tavus API Key: ")
    api_key = cli.launch()
    print(f"Tavus API key: {api_key}")
    
    # Initialize API client
    api_client = TavusAPIClient(api_key)

def execute_set_api_key():
  """Execute set API key and return next state"""
  print("\n=== Set API Key ===")
  global api_key, api_client

  print("Currently set API key: ", api_key)
  cli = YesNo(prompt="Would you like to set a new API key?", default="n")
  if cli.launch():
    cli = Input(prompt="Enter your new Tavus API Key: ")
    api_key = cli.launch()
    print(f"Tavus API key: {api_key}")
    
    api_client = TavusAPIClient(api_key)

  return State.MAIN_MENU

def execute_work_with_replicas():
  """Execute work with replicas menu and return next state"""
  print("\n=== Work with Replicas ===")
  
  with yaspin(text="Loading replicas..."):
    update_replicas()

  cli = Bullet(
    prompt="What would you like to do with Replicas?",
    choices=["Create a Replica", "List Replicas", "Modify a Replica", "Delete a Replica", "Back to Main Menu"],
    bullet="🧑",
    margin=2,
    shift=0,
  )
  result = cli.launch()

  if result == "Create a Replica":
    return State.CREATE_REPLICA
  elif result == "List Replicas":
    return State.LIST_REPLICAS
  elif result == "Modify a Replica":
    return State.MODIFY_REPLICA
  elif result == "Delete a Replica":
    return State.DELETE_REPLICA
  elif result == "Back to Main Menu":
    return State.MAIN_MENU
  else:
    return State.WORK_WITH_REPLICAS

def execute_work_with_personas():
  """Execute work with personas menu and return next state"""
  print("\n=== Work with Personas ===")
  
  with yaspin(text="Loading personas..."):
    update_personas()
    
  cli = Bullet(
    prompt="What would you like to do with Personas?",
    choices=["Create a Persona", "List Personas", "Delete a Persona", "Back to Main Menu"],
    bullet="🧑",
    margin=2,
    shift=0,
  )
  result = cli.launch()

  if result == "Create a Persona":
    return State.CREATE_PERSONA
  elif result == "List Personas":
    return State.LIST_PERSONAS
  elif result == "Delete a Persona":
    return State.DELETE_PERSONA
  elif result == "Back to Main Menu":
    return State.MAIN_MENU
  else:
    return State.WORK_WITH_PERSONAS

def execute_create_replica():
  """Execute create replica functionality and return next state"""
  print("\n=== Create Replica ===")
  print("Create replica functionality will be implemented here...")
  # TODO: Implement create replica logic
  return State.WORK_WITH_REPLICAS

def execute_list_replicas():
  """Execute list replicas functionality and return next state"""
  global replicas
  print("\n=== List Replicas ===")
  
  if api_client is None:
    print("Error: API client not initialized. Please set your API key first.")
    return State.MAIN_MENU
  
  success, message, replicas = api_client.fetch_replicas()
  if success:
    print(message)
    if not replicas:
      print("No replicas found.")
    else:
      for i, replica in enumerate(replicas, 1):
        replica_id = replica.get('replica_id', 'N/A')
        replica_name = replica.get('replica_name', 'N/A')
        replica_type = replica.get('replica_type', 'N/A')
        status = replica.get('status', 'N/A')
        training_progress = replica.get('training_progress', 'N/A')
        created_at = replica.get('created_at', 'N/A')
        
        print(f"{i}. Replica ID: {replica_id}")
        print(f"   Name: {replica_name}")
        print(f"   Type: {replica_type}")
        print(f"   Status: {status}")
        print(f"   Training Progress: {training_progress}")
        print(f"   Created: {created_at}")
        print()
  else:
    print(message)

  return State.WORK_WITH_REPLICAS

def execute_modify_replica():
  """Execute modify replica functionality and return next state"""
  print("\n=== Modify Replica ===")
  print("Modify replica functionality will be implemented here...")
  # TODO: Implement modify replica logic
  return State.WORK_WITH_REPLICAS

def execute_delete_replica():
  """Execute delete replica functionality and return next state"""
  print("\n=== Delete Replica ===")
  print("Delete replica functionality will be implemented here...")
  # TODO: Implement delete replica logic
  return State.WORK_WITH_REPLICAS

def execute_create_persona():
  """Execute create persona functionality and return next state"""
  print("\n=== Create Persona ===")
  print("Create persona functionality will be implemented here...")
  # TODO: Implement create persona logic
  return State.WORK_WITH_PERSONAS

def execute_list_personas():
  """Execute list personas functionality and return next state"""
  print("\n=== List Personas ===")
  print("List personas functionality will be implemented here...")
  # TODO: Implement list personas logic
  return State.WORK_WITH_PERSONAS

def execute_delete_persona():
  """Execute delete persona functionality and return next state"""
  print("\n=== Delete Persona ===")
  print("Delete persona functionality will be implemented here...")
  # TODO: Implement delete persona logic
  return State.WORK_WITH_PERSONAS

def update_replicas():
  global replicas
  global api_client

  if api_client is None:
    print("Error: API client not initialized. Please set your API key first.")
    return

  success, message, fetched_replicas = api_client.fetch_replicas()
  if success:
    replicas = fetched_replicas
  else:
    print(message)

def update_personas():
  global personas
  global api_client
  
  if api_client is None:
    print("Error: API client not initialized. Please set your API key first.")
    return

  success, message, fetched_personas = api_client.fetch_personas()
  if success:
    personas = fetched_personas
  else:
    print(message)

if __name__ == "__main__":
  main()