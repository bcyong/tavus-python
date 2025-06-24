#!/usr/bin/env python3

from bullet import Input
import os
from api_client import TavusAPIClient
from state_machine import StateMachine
from yaspin import yaspin

def main():
  print("Welcome to the Tavus Python CLI Tool!")

  # Initialize state machine
  state_machine = StateMachine()
  
  # Set initial API key
  set_initial_api_key(state_machine)

  print("Updating replicas and personas...")
  with yaspin(text="Loading replicas..."):
    state_machine.update_replicas()
  with yaspin(text="Loading personas..."):
    state_machine.update_personas()
  print("Initialization complete!")

  # State machine loop
  while not state_machine.is_exit_state():
    state_machine.execute_current_state()

def set_initial_api_key(state_machine):
  """Set the initial API key from .tavus_api_key file"""
  if os.path.exists(".tavus_api_key"):
    with open(".tavus_api_key", "r") as file:
      api_key = file.read().strip()
      api_client = TavusAPIClient(api_key)
      state_machine.set_api_client(api_client)
      state_machine.set_api_key(api_key)
  else:
    cli = Input(prompt="Enter your Tavus API Key: ")
    api_key = cli.launch()
    print(f"Tavus API key: {api_key}")
    
    # Initialize API client
    api_client = TavusAPIClient(api_key)
    state_machine.set_api_client(api_client)
    state_machine.set_api_key(api_key)

if __name__ == "__main__":
  main()