import socket
import concurrent.futures
import os
import requests

from rich.table import Table
from rich.console import Console 
from rich.panel import Panel
from rich.text import Text
from pyfiglet import Figlet
from rich.console import Group


console = Console()


#terminal title
os.system("title RScanner")


#creating my banner
def welcome(count):

    f = Figlet(font="big")
    banner_text = f.renderText("RS  SCANNER")
    text = Text(banner_text, justify="center",style="bold blue")

    grid = Table.grid(expand=True)
    grid.add_column(justify="left")

    grid.add_row(
        f"[bold blue]Scans Completed: {count}", 
    )

    content = Group(text, Text("\n"), grid)
    
    panel = Panel(content, title="WELCOME", subtitle="v1.8", border_style="bold magenta")
    console.print(panel)


#domain ip location
def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = response.json()
        if data['status'] == 'success':
            return data['city'], data['country']
        return "Unknown", "Unknown"
    except:
        return "Unknown", "Unknown"


#domain resolution
def get_target():
    while True:
        choice = console.input("\n[bold yellow]Enter target Domain: ").strip().lower()
        try:
                target = socket.gethostbyname(choice)
                city,country = get_location(target)

                domain_table=Table(title="Domain Resolution",show_header=True,title_style="bold magenta")
                domain_table.add_column("Domain Name",style="bold green",justify="center")
                domain_table.add_column("IP Address",style="bold green", justify="center")
                domain_table.add_column("City",style="bold green", justify="center")
                domain_table.add_column("Country",style="bold green",justify="center")

                domain_table.add_row(choice,target,city,country)
                console.print("\n",domain_table)

                return target
        
        except socket.gaierror:
            console.print("\n[bold red]Cannot find domain,add a new domain.")



#scanner menu
def get_scan_mode():

    menu_table = Table(title="Scan Types",show_header=True,title_style="bold magenta")
    menu_table.add_column("Choice", style="bold green", justify="center")
    menu_table.add_column("Type", style="bold green", justify="center")
    menu_table.add_column("Range", style="bold green", justify="center")
    

    menu_table.add_row("1", "Common Ports","1-1023")
    menu_table.add_row("2", "Full Scan","1-65535")
    
    console.print(menu_table)

    while True:
        choice = console.input("\n[bold yellow]Enter your choice (1 or 2):").strip()
        
        if choice == '1':
            console.print() #space

            console.print(Panel(
                "[gold1]Selected: Common Ports Scan (1-1023)",
                border_style="gold1",
                expand=False  
            ))
            return range(1, 1024) 
            
        elif choice == '2':
            console.print()

            console.print(Panel(
                "[bold red]Selected: Full Scan (1-65535) - This will take time",
                border_style="red",
                expand=False
            ))
            return range(1, 65536)
            
        else:
            console.print("\n[bold red]Invalid choice,please enter 1 or 2.")


#socket connection
def check_port(target,port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srch:
            srch.settimeout(0.1)
            res = srch.connect_ex((target, port))
            if res == 0:
                return port #Returns the number,does not print every port scanned
            else:
                return None 
    except Exception:
        return None 


def scan_ports(target,ports):
    console.print(Panel(
        f"[gold1]Scanning {len(ports)} ports on {target}",
        border_style="gold1",
        expand=False
    ))


    #Manual list to ensure common ports don't show as "Unknown"
    PORT_DATA = {
        21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp",
        53: "dns", 80: "http", 110: "pop3", 111: "rpcbind",
        135: "msrpc", 139: "netbios-ssn", 143: "imap", 443: "https",
        445: "microsoft-ds", 465: "smtps", 587: "smpts", 
        993: "imaps", 995: "pop3s", 1433: "mssql", 1521: "oracle",
        3306: "mysql", 3389: "rdp", 5432: "postgresql", 5900: "vnc",
        6379: "redis", 8000: "http-alt", 8080: "http-proxy", 
        8443: "https-alt", 27017: "mongodb"
    }


    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        futures = {executor.submit(check_port, target, port): port for port in ports}

        for future in concurrent.futures.as_completed(futures):
            port = futures[future]
            if future.result():
                open_ports.append(port)

    open_ports.sort()


    if open_ports:
        table = Table(title="\nScan Result",show_header=True,title_style="bold magenta")
        table.add_column("Port", style="bold cyan", justify="center")
        table.add_column("Service", style="bold blue", justify="center")
        table.add_column("Status", style="bold green", justify="center")
        
        for port in open_ports:
            #Check our Manual List first (Fixes Unknowns)
            if port in PORT_DATA:
                service_name = PORT_DATA[port]
            else:
                try:
                    service_name = socket.getservbyport(port, "tcp")
                except:
                    service_name = "Unknown"
            
            table.add_row(str(port), service_name, "OPEN")
        
        console.print(table)
    else:
        console.print("[red]No open ports found.[/red]")

    console.print() #space
    console.print(Panel(
        "[bold green]Scan Completed Successfully!",
        border_style="green",
        expand=False
    ))


    #statistics of the scan
    total_scanned = len(ports)
    open_count = len(open_ports)
    
    stats_message = f"[bold red]{open_count}[/bold red] ports found open out of [bold red]{total_scanned}[/bold red] scanned"
    
    console.print() #space
    console.print(Panel(
        stats_message,
        title="[bold magenta]Scan Statistics",
        border_style="green",
        expand=False
    ))

    return open_ports

#ontrols the main program flow
def main():
 
 count=0

 while True:
        # Clear screen for a fresh start
        os.system('cls' if os.name == 'nt' else 'clear')
        
        welcome(count)

        target = get_target()
        ports = get_scan_mode()
        scan_ports(target,ports)

        count+=1

        while True:
            choice = console.input("\n[bold yellow]Press R to Run Again or X to Exit: ").strip().lower()
            
            if choice == 'r':
                break 
            elif choice == 'x':
                console.print("\n[bold red]Goodbye!!")
                console.input("\n[dim]Press Enter to close window...[/dim]")
                return
            else:
                continue


if __name__ == "__main__":
    main()
