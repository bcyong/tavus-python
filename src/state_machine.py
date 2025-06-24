#!/usr/bin/env python3

from bullet import Input, Bullet, YesNo
from yaspin import yaspin
from enum import Enum
from api_client import TavusAPIClient
from models import Replica, Persona

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
    self.replicas = []  # List of Replica objects
    self.personas = []  # List of Persona objects
  
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
      bullet="→",
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

    return self.show_paginated_replicas()

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
    
    if self.api_client is None:
      print("Error: API client not initialized. Please set your API key first.")
      return State.MAIN_MENU

    return self.show_paginated_personas()

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
      # Convert dictionary data to Replica objects
      self.replicas = [Replica.from_dict(replica_data) for replica_data in fetched_replicas]
    else:
      print(message)

  def update_personas(self):
    """Update the personas list from API"""
    if self.api_client is None:
      print("Error: API client not initialized. Please set your API key first.")
      return

    success, message, fetched_personas = self.api_client.fetch_personas()
    if success:
      # Convert dictionary data to Persona objects
      self.personas = [Persona.from_dict(persona_data) for persona_data in fetched_personas]
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

  def print_replicas(self):
    """Print the replicas list using short display format"""
    if not self.replicas:
      print("No replicas found.")
      return
    
    print(f"Found {len(self.replicas)} replica(s):\n")
    for i, replica in enumerate(self.replicas, 1):
      print(f"{i}. {replica.display_short()}")

  def print_personas(self):
    """Print the personas list using short display format"""
    if not self.personas:
      print("No personas found.")
      return
    
    print(f"Found {len(self.personas)} persona(s):\n")
    for i, persona in enumerate(self.personas, 1):
      print(f"{i}. {persona.display_short()}")

  def show_paginated_replicas(self, page=0, items_per_page=10, filter_type="all"):
    """Show paginated list of replicas with selection"""
    if not self.replicas:
      print("No replicas found.")
      input("Press Enter to continue...")
      return State.WORK_WITH_REPLICAS

    # Filter replicas based on type
    if filter_type == "user":
      filtered_replicas = [r for r in self.replicas if r.replica_type == "user"]
      sectioned_replicas = [filtered_replicas]
      section_names = ["User Replicas"]
    elif filter_type == "system":
      filtered_replicas = [r for r in self.replicas if r.replica_type == "system"]
      sectioned_replicas = [filtered_replicas]
      section_names = ["System Replicas"]
    else:  # "all"
      user_replicas = [r for r in self.replicas if r.replica_type == "user"]
      system_replicas = [r for r in self.replicas if r.replica_type == "system"]
      filtered_replicas = user_replicas + system_replicas
      sectioned_replicas = [user_replicas, system_replicas]
      section_names = ["User Replicas", "System Replicas"]

    if not filtered_replicas:
      print(f"No {filter_type} replicas found.")
      input("Press Enter to continue...")
      return State.WORK_WITH_REPLICAS

    total_pages = (len(filtered_replicas) - 1) // items_per_page
    start_idx = page * items_per_page
    end_idx = min(start_idx + items_per_page, len(filtered_replicas))
    current_replicas = filtered_replicas[start_idx:end_idx]

    print(f"\nPage {page + 1} of {total_pages + 1} ({len(filtered_replicas)} {filter_type} replicas)")
    print("=" * 50)

    # Build choices list
    choices = []
    
    # Add filter options at the top
    choices.append(f"Current filter: {filter_type}")
    
    # Add navigation options
    if page > 0:
      choices.append("← Previous Page")
    
    # Add replica items with section headers for "all" view
    if filter_type == "all":
      current_idx = start_idx
      for section_idx, (section_replicas, section_name) in enumerate(zip(sectioned_replicas, section_names)):
        if section_replicas:  # Only show section if it has replicas
          # Check if this section has items on current page
          section_start = current_idx
          section_end = current_idx + len(section_replicas)
          
          if section_start < end_idx and section_end > start_idx:
            # Add section header
            choices.append(f"--- {section_name} ---")
            
            # Add items from this section that are on current page
            for i, replica in enumerate(section_replicas):
              global_idx = current_idx + i + 1
              if start_idx < global_idx <= end_idx:
                choices.append(f"{global_idx}. {replica.display_short()}")
          
          current_idx += len(section_replicas)
    else:
      # Single section view (user or system only)
      for i, replica in enumerate(current_replicas, start_idx + 1):
        choices.append(f"{i}. {replica.display_short()}")
    
    # Add navigation options
    if page < total_pages:
      choices.append("→ Next Page")
    
    choices.append("← Go Back")

    # Show menu
    cli = Bullet(
      prompt="Select a replica to view details or navigate:",
      choices=choices,
      bullet="→",
      margin=2,
      shift=0,
    )
    result = cli.launch()

    # Handle filter selection
    if result == f"Current filter: {filter_type}":
      return self.show_filter_selection()
    
    # Handle navigation
    if result == "← Previous Page":
      return self.show_paginated_replicas(page - 1, items_per_page, filter_type)
    elif result == "→ Next Page":
      return self.show_paginated_replicas(page + 1, items_per_page, filter_type)
    elif result == "← Go Back":
      return State.WORK_WITH_REPLICAS
    
    # Handle replica selection
    if result.startswith("→") or result.startswith("---"):
      return self.show_paginated_replicas(page, items_per_page, filter_type)
    
    # Extract replica index from selection
    try:
      replica_idx = int(result.split('.')[0]) - 1
      if 0 <= replica_idx < len(filtered_replicas):
        self.show_replica_details(filtered_replicas[replica_idx])
        input("Press Enter to continue...")
        return self.show_paginated_replicas(page, items_per_page, filter_type)
    except (ValueError, IndexError):
      pass
    
    return self.show_paginated_replicas(page, items_per_page, filter_type)

  def show_filter_selection(self):
    """Show filter selection for replicas"""
    print("\n=== Filter Replicas ===")
    
    cli = Bullet(
      prompt="Select filter type:",
      choices=["user only", "system only", "all replicas"],
      bullet="→",
      margin=2,
      shift=0,
    )
    result = cli.launch()

    if result == "user only":
      return self.show_paginated_replicas(filter_type="user")
    elif result == "system only":
      return self.show_paginated_replicas(filter_type="system")
    elif result == "all replicas":
      return self.show_paginated_replicas(filter_type="all")
    
    return self.show_paginated_replicas()

  def show_paginated_personas(self, page=0, items_per_page=10):
    """Show paginated list of personas with selection"""
    if not self.personas:
      print("No personas found.")
      input("Press Enter to continue...")
      return State.WORK_WITH_PERSONAS

    total_pages = (len(self.personas) - 1) // items_per_page
    start_idx = page * items_per_page
    end_idx = min(start_idx + items_per_page, len(self.personas))
    current_personas = self.personas[start_idx:end_idx]

    print(f"\nPage {page + 1} of {total_pages + 1} ({len(self.personas)} total personas)")
    print("=" * 50)

    # Build choices list
    choices = []
    
    # Add navigation options
    if page > 0:
      choices.append("← Previous Page")
    
    # Add persona items
    for i, persona in enumerate(current_personas, start_idx + 1):
      choices.append(f"{i}. {persona.display_short()}")
    
    # Add navigation options
    if page < total_pages:
      choices.append("→ Next Page")
    
    choices.append("← Go Back")

    # Show menu
    cli = Bullet(
      prompt="Select a persona to view details or navigate:",
      choices=choices,
      bullet="→",
      margin=2,
      shift=0,
    )
    result = cli.launch()

    # Handle navigation
    if result == "← Previous Page":
      return self.show_paginated_personas(page - 1, items_per_page)
    elif result == "→ Next Page":
      return self.show_paginated_personas(page + 1, items_per_page)
    elif result == "← Go Back":
      return State.WORK_WITH_PERSONAS
    
    # Handle persona selection
    if result.startswith("→"):
      return self.show_paginated_personas(page, items_per_page)
    
    # Extract persona index from selection
    try:
      persona_idx = int(result.split('.')[0]) - 1
      if 0 <= persona_idx < len(self.personas):
        self.show_persona_details(self.personas[persona_idx])
        input("Press Enter to continue...")
        return self.show_paginated_personas(page, items_per_page)
    except (ValueError, IndexError):
      pass
    
    return self.show_paginated_personas(page, items_per_page)

  def show_replica_details(self, replica):
    """Show detailed information for a specific replica"""
    print("\n" + "=" * 60)
    print("REPLICA DETAILS")
    print("=" * 60)
    print(replica.display_verbose())
    print("=" * 60)

  def show_persona_details(self, persona):
    """Show detailed information for a specific persona"""
    print("\n" + "=" * 60)
    print("PERSONA DETAILS")
    print("=" * 60)
    print(persona.display_verbose())
    print("=" * 60)