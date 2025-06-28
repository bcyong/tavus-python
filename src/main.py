#!/usr/bin/env python3

import os
import click
from bullet import Input
from yaspin import yaspin

from api_client import TavusAPIClient
from state_machine_modular import StateMachineModular

@click.command()
@click.option('--api-key-file', '-f', 
              default='.tavus_api_key',
              help='Path to file containing the Tavus API key (default: .tavus_api_key)')
def main(api_key_file):
  print("Welcome to the Tavus Python CLI Tool!")

  # Initialize state machine
  state_machine = StateMachineModular()
  
  # Set initial API key
  set_initial_api_key(state_machine, api_key_file)

  print("Initialization complete!")

  # State machine loop
  while not state_machine.is_exit_state():
    state_machine.execute_current_state()

def set_initial_api_key(state_machine, api_key_file):
  """Set the initial API key from the specified file"""
  if os.path.exists(api_key_file):
    with open(api_key_file, "r") as file:
      api_key = file.read().strip()
      api_client = TavusAPIClient(api_key)
      state_machine.set_api_client(api_client)
      state_machine.set_api_key(api_key)
  else:
    cli = Input(prompt="Enter your Tavus API Key: ")
    api_key = cli.launch()
    if api_key:  # Add null check
      print(f"Tavus API key: {api_key}")
      
      # Initialize API client
      api_client = TavusAPIClient(api_key)
      state_machine.set_api_client(api_client)
      state_machine.set_api_key(api_key)
    else:
      print("No API key provided. You can set it later from the main menu.")

if __name__ == "__main__":
  main()