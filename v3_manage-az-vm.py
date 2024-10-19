import subprocess
import os
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

def get_vm_list(file_name):
    with open(file_name, 'r') as file:
        vm_list = [line.strip() for line in file if line.strip()]
    return vm_list

def get_vm_details(resource_id):
    query = "[name, (instanceView.statuses[?code.starts_with(@, 'PowerState/')].displayStatus | [0])]"
    command = f'az vm get-instance-view --ids {resource_id} --query "{query}" -o tsv'
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True).strip().split('\n')
        name = output[0] if output else "Unknown"
        power_state = output[1] if len(output) > 1 else "Unavailable"
        return name, power_state
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return "Unknown", "Error"

def start_vm(resource_id):
    command = f'az vm start --ids {resource_id}'
    subprocess.run(command, shell=True, check=True)

def deallocate_vm(resource_id):
    command = f'az vm deallocate --ids {resource_id}'
    subprocess.run(command, shell=True, check=True)

def get_valid_resource_id(prompt, vm_status_data):
    while True:
        vm_number = input(prompt).strip()
        if vm_number.isdigit() and 1 <= int(vm_number) <= len(vm_status_data):
            return vm_status_data[int(vm_number) - 1][3]  # Return the resource ID
        print("Invalid VM number. Please try again.")

def confirm_action(action):
    return input(f"Are you sure you want to {action} this VM? (y/n): ").lower() == 'y'

def scan_vm_status(console, vm_list):
    vm_status_data = []
    total_vms = len(vm_list)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Scanning VM status...", total=total_vms)

        for i, resource_id in enumerate(vm_list, 1):
            name, power_state = get_vm_details(resource_id)
            vm_status_data.append((i, name, power_state, resource_id))
            progress.update(task, advance=1)

    console.print("[green]VM status scan completed.[/green]")
    return vm_status_data

def display_vm_status(console, vm_status_data, filter_option='all'):
    table = Table(title=f"VM Status Summary ({filter_option.capitalize()})")
    table.add_column("VM", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Power State", style="green")

    filtered_vms = []
    for vm in vm_status_data:
        if filter_option == 'all' or \
           (filter_option == 'running' and vm[2].lower() == 'vm running') or \
           (filter_option == 'deallocated' and vm[2].lower() == 'vm deallocated'):
            table.add_row(f"[cyan]{vm[0]}[/cyan]", vm[1], vm[2])
            filtered_vms.append(vm)

    console.print(table)
    return filtered_vms

def manage_vms_after_filter(console, filtered_vms, filter_option, vm_status_data):
    if filter_option == 'deallocated' and filtered_vms:
        if input("Do you want to start a VM? (y/n): ").lower() == 'y':
            resource_id = get_valid_resource_id("Enter the VM number to start: ", filtered_vms)
            if confirm_action("start"):
                try:
                    start_vm(resource_id)
                    console.print("[green]VM start initiated.[/green]")
                except subprocess.CalledProcessError as e:
                    console.print(f"[red]Error starting VM: {e}[/red]")
    elif filter_option == 'running' and filtered_vms:
        if input("Do you want to stop and deallocate a VM? (y/n): ").lower() == 'y':
            resource_id = get_valid_resource_id("Enter the VM number to stop and deallocate: ", filtered_vms)
            if confirm_action("stop and deallocate"):
                try:
                    deallocate_vm(resource_id)
                    console.print("[green]VM deallocation initiated.[/green]")
                except subprocess.CalledProcessError as e:
                    console.print(f"[red]Error deallocating VM: {e}[/red]")

def main():
    console = Console()

    while True:
        file_name = input("Enter the file name containing the VM resource IDs (default: 'manage_vmlist.txt'): ").strip()
        if not file_name:
            file_name = 'manage_vmlist.txt'
        if os.path.exists(file_name):
            break
        console.print(f"[red]Error: File '{file_name}' not found. Please try again.[/red]")

    try:
        vm_list = get_vm_list(file_name)
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")
        return

    vm_status_data = None
    options = ["Scan and View Status", "Exit"]

    while True:
        console.print("\nSelect an option:")
        for i, option in enumerate(options, 1):
            console.print(f"{i}. {option}")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            console.print("[red]Invalid input. Please enter a number corresponding to the options.[/red]")
            continue

        if choice == 1:  # Scan and View Status
            vm_status_data = scan_vm_status(console, vm_list)
            
            while True:
                filter_options = ['all', 'running', 'deallocated']
                console.print("\nSelect a filter option:")
                for i, option in enumerate(filter_options, 1):
                    console.print(f"{i}. Show {option}")
                console.print("4. Return to main menu")
                
                try:
                    filter_choice = int(input("Enter your filter choice: "))
                    if 1 <= filter_choice <= 3:
                        filtered_vms = display_vm_status(console, vm_status_data, filter_options[filter_choice - 1])
                        manage_vms_after_filter(console, filtered_vms, filter_options[filter_choice - 1], vm_status_data)
                    elif filter_choice == 4:
                        break
                    else:
                        console.print("[red]Invalid filter option. Please try again.[/red]")
                except ValueError:
                    console.print("[red]Invalid input. Please enter a number.[/red]")

        elif choice == 2:  # Exit
            console.print("[yellow]Exiting the script.[/yellow]")
            break
        else:
            console.print("[red]Invalid option. Please choose a number between 1 and 2.[/red]")

if __name__ == "__main__":
    main()