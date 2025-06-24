#!/usr/bin/env python3

from bullet import Input, Bullet, YesNo
from yaspin import yaspin
from enum import Enum
from api_client import TavusAPIClient

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

class StateMachine:
  def __init__(self):
    self.api_client = None
    self.api_key = None
    self.current_state = State.MAIN_MENU
    self.replicas = []
    self.personas = []
  
  def execute_current_state(self):
    """Execute the current state and update the next state"""
    if self.current_state == State.MAIN_MENU:
      self.current_state = self.execute_main_menu()
    elif self.current_state == State.SET_API_KEY:
      self.current_state = self.execute_set_api_key()
    elif self.current_state == State.WORK_WITH_REPLICAS:
      self.current_state = self.execute_work_with_replicas()
    elif self.current_state == State.WORK_WITH_PERSONAS:
      self.current_state = self.execute_work_with_personas()
    elif self.current_state == State.CREATE_REPLICA:
      self.current_state = self.execute_create_replica()
    elif self.current_state == State.LIST_REPLICAS:
      self.current_state = self.execute_list_replicas()
    elif self.current_state == State.MODIFY_REPLICA:
      self.current_state = self.execute_modify_replica()
    elif self.current_state == State.DELETE_REPLICA:
      self.current_state = self.execute_delete_replica()
    elif self.current_state == State.CREATE_PERSONA:
      self.current_state = self.execute_create_persona()
    elif self.current_state == State.LIST_PERSONAS:
      self.current_state = self.execute_list_personas()
    elif self.current_state == State.DELETE_PERSONA:
      self.current_state = self.execute_delete_persona()
    else:
      print(f"Unknown state: {self.current_state}")
      self.current_state = State.MAIN_MENU
  
  def execute_main_menu(self):
    """Execute main menu and return next state"""
    print("\n=== Main Menu ===")
    print(f"Tavus API key: {self.api_key}")
    
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

  def execute_set_api_key(self):
    """Execute set API key and return next state"""
    print("\n=== Set API Key ===")
    print("Currently set API key: ", self.api_key)
    cli = YesNo(prompt="Would you like to set a new API key?", default="n")
    if cli.launch():
      cli = Input(prompt="Enter your new Tavus API Key: ")
      self.api_key = cli.launch()
      print(f"Tavus API key: {self.api_key}")
      
      self.api_client = TavusAPIClient(self.api_key)

    return State.MAIN_MENU

  def execute_work_with_replicas(self):
    """Execute work with replicas menu and return next state"""
    print("\n=== Work with Replicas ===")
    
    with yaspin(text="Loading replicas..."):
      self.update_replicas()

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

  def execute_work_with_personas(self):
    """Execute work with personas menu and return next state"""
    print("\n=== Work with Personas ===")
    
    with yaspin(text="Loading personas..."):
      self.update_personas()

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

  def execute_create_replica(self):
    """Execute create replica functionality and return next state"""
    print("\n=== Create Replica ===")
    print("Create replica functionality will be implemented here...")
    # TODO: Implement create replica logic
    return State.WORK_WITH_REPLICAS

  def execute_list_replicas(self):
    """Execute list replicas functionality and return next state"""
    print("\n=== List Replicas ===")
    
    if self.api_client is None:
      print("Error: API client not initialized. Please set your API key first.")
      return State.MAIN_MENU
    
    success, message, self.replicas = self.api_client.fetch_replicas()
    if success:
      print(message)
      if not self.replicas:
        print("No replicas found.")
      else:
        for i, replica in enumerate(self.replicas, 1):
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

  def execute_modify_replica(self):
    """Execute modify replica functionality and return next state"""
    print("\n=== Modify Replica ===")
    print("Modify replica functionality will be implemented here...")
    # TODO: Implement modify replica logic
    return State.WORK_WITH_REPLICAS

  def execute_delete_replica(self):
    """Execute delete replica functionality and return next state"""
    print("\n=== Delete Replica ===")
    print("Delete replica functionality will be implemented here...")
    # TODO: Implement delete replica logic
    return State.WORK_WITH_REPLICAS

  def execute_create_persona(self):
    """Execute create persona functionality and return next state"""
    print("\n=== Create Persona ===")
    print("Create persona functionality will be implemented here...")
    # TODO: Implement create persona logic
    return State.WORK_WITH_PERSONAS

  def execute_list_personas(self):
    """Execute list personas functionality and return next state"""
    print("\n=== List Personas ===")
    print("List personas functionality will be implemented here...")
    # TODO: Implement list personas logic
    return State.WORK_WITH_PERSONAS

  def execute_delete_persona(self):
    """Execute delete persona functionality and return next state"""
    print("\n=== Delete Persona ===")
    print("Delete persona functionality will be implemented here...")
    # TODO: Implement delete persona logic
    return State.WORK_WITH_PERSONAS

  def update_replicas(self):
    """Update the replicas list from API"""
    if self.api_client is None:
      print("Error: API client not initialized. Please set your API key first.")
      return

    success, message, fetched_replicas = self.api_client.fetch_replicas()
    if success:
      self.replicas = fetched_replicas
    else:
      print(message)

  def update_personas(self):
    """Update the personas list from API"""
    if self.api_client is None:
      print("Error: API client not initialized. Please set your API key first.")
      return

    success, message, fetched_personas = self.api_client.fetch_personas()
    if success:
      self.personas = fetched_personas
    else:
      print(message)

  def set_api_client(self, api_client):
    """Set the API client instance"""
    self.api_client = api_client

  def set_api_key(self, api_key):
    """Set the API key"""
    self.api_key = api_key

  def is_exit_state(self):
    """Check if current state is exit"""
    return self.current_state == State.EXIT 