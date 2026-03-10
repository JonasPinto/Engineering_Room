import os
import sys
import time
import ast
import array
import random
import platform
from pympler import asizeof

# Importing Rich library components
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt
from rich.align import Align
from rich.text import Text
from rich.columns import Columns

# Initializing Rich console
console = Console()
THEME_COLOR = "blue"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header(title, subtitle=None, style=f"bold {THEME_COLOR}"):
    clear_screen()
    content = Text(title, style=style)
    if subtitle:
        content.append(f"\n{subtitle}", style="dim white")
    panel = Panel(Align.center(content), border_style=THEME_COLOR, padding=(1, 2))
    console.print(panel)

def get_system_info():
    """Exibe o Dashboard do sistema com largura total."""
    info_text = Text.assemble(
        ("OS: ", "dim"), (f"{platform.system()} {platform.release()}  ", "white"),
        ("Python: ", "dim"), (f"{platform.python_version()}  ", "white")
    )
    return Panel(
        info_text, 
        title="[bold white]SYSTEM DASHBOARD[/bold white]", 
        border_style="dim", 
        padding=(0, 1),
        expand=True
    )

def run_benchmark(data_choice, base_val):
    """Simulação massiva com lógica hardened para 2.5 milhões de itens."""
    show_header("MASSIVE DATA SIMULATION")
    
    items_count = 2500000 
    data_type_name = { "1": "integers", "2": "floats", "3": "objects/replicas" }[data_choice]
    
    console.print(f"\n[bold white]BENCHMARK OVERVIEW:[/bold white]")
    console.print(f"Simulating [bold cyan]{items_count:,}[/bold cyan] {data_type_name}...")
    input(f"\n[bold white]»[/bold white] Press ENTER to begin simulation...")

    with Progress(
        SpinnerColumn(), 
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        TaskProgressColumn(),
        console=console,
        transient=False,
    ) as progress:
        task = progress.add_task(description="Processing...", total=100)
        
        steps = ["Allocating Memory Blocks", "Serializing Objects", "Simulating Disk I/O", "Finalizing Analysis"]
        for step in steps:
            progress.update(task, description=f"[cyan]{step}...[/cyan]")
            for _ in range(25):
                time.sleep(0.01)
                progress.update(task, advance=1)

    # Lógica de cálculo técnica (Baseada em arquitetura 64-bit)
    ptr_size = 8  # Tamanho de um ponteiro (Address size)
    
    if data_choice == "1": # Integers
        obj_size = sys.getsizeof(10**9) # ~28 bytes em Python
        # RAM = (Lista de ponteiros) + (Instâncias de objetos inteiros)
        size_list = (ptr_size * items_count) + (obj_size * items_count)
        size_optimized = 8 * items_count # uint64 bruto
        disk_size_csv = 11 * items_count 
        disk_size_bin = 8 * items_count
        
    elif data_choice == "2": # Floats
        obj_size = sys.getsizeof(1.1) # 24 bytes
        size_list = (ptr_size * items_count) + (obj_size * items_count)
        size_optimized = 8 * items_count # double bruto
        disk_size_csv = 18 * items_count 
        disk_size_bin = 8 * items_count
        
    else: # Complex Objects / Collections
        deep_obj_size = asizeof.asizeof(base_val)
        # RAM = (Ponteiros) + (Objetos únicos na memória)
        size_list = (ptr_size * items_count) + (deep_obj_size * items_count)
        size_optimized = size_list * 0.4 
        disk_size_csv = (len(str(base_val)) + 1) * items_count
        disk_size_bin = (deep_obj_size * 0.7) * items_count

    def to_mb(b): return b / (1024 * 1024)

    # Tabela de Resultados do Benchmark
    unified_table = Table(title=f"RESOURCES FOR 2.5 MILLION ITEMS", border_style=THEME_COLOR, header_style=f"bold {THEME_COLOR}")
    unified_table.add_column("RESOURCE", style="bold white")
    unified_table.add_column("METHOD / FORMAT", style="dim")
    unified_table.add_column("CONSUMPTION", justify="right")
    
    unified_table.add_row("RAM MEMORY", "Standard Python List", f"[red]{to_mb(size_list):>10.2f} MB[/red]")
    unified_table.add_row("", "Optimized C-Structure", f"[bold green]{to_mb(size_optimized):>10.2f} MB[/bold green]")
    unified_table.add_section()
    unified_table.add_row("DISK STORAGE", "Plain Text (CSV/TXT)", f"[red]{to_mb(disk_size_csv):>10.2f} MB[/red]")
    unified_table.add_row("", "Raw Binary Format", f"[bold green]{to_mb(disk_size_bin):>10.2f} MB[/bold green]")

    console.print(unified_table)

    # Cálculos de eficiência para o Insight
    economy_ram = ((size_list - size_optimized) / size_list) * 100
    economy_disk = ((disk_size_csv - disk_size_bin) / disk_size_csv) * 100
    
    console.print(f"\n[bold yellow]TECHNICAL AUDIT RESULTS:[/bold yellow]")
    console.print(f" • [bold green]{economy_ram:.1f}% RAM savings[/bold green] by reducing object overhead.")
    console.print(f" • [bold green]{economy_disk:.1f}% Disk savings[/bold green] via binary serialization.")

    insight = (
        "\n[bold cyan]SCALABILITY INSIGHT:[/bold cyan]\n"
        "At 2.5M records, contiguous memory allocation prevents high latency caused by pointer indirection."
    )
    console.print(insight)
    
    Prompt.ask(f"\n[dim]Press ENTER to return...[/dim]", default="", show_default=False)

def run_inspector():
    """Analisa um único dado e oferece transição para benchmark."""
    examples = [
        Panel("[cyan](10, 20)[/cyan]\n[dim]Tuple[/dim]", border_style="dim"),
        Panel("[green]'name'[/green]\n[dim]String[/dim]", border_style="dim"),
        Panel("[yellow][1, 2, 3][/yellow]\n[dim]List[/dim]", border_style="dim"), 
        Panel("[red]2506[/red]\n[dim]Integer[/dim]", border_style="dim"),
        Panel("[magenta]1.89[/magenta]\n[dim]Float[/dim]", border_style="dim"),
        Panel("[blue]{1, 2}[/blue]\n[dim]Set[/dim]", border_style="dim"),
    ]
    console.print("[bold white]Input Examples:[/bold white]")
    console.print(Columns(examples))
    
    # Validação de entrada vazia
    raw_input = ""
    while not raw_input:
        raw_input = Prompt.ask(f"\n[bold white]Enter a value to analyze[/bold white]").strip()
        if not raw_input:
            console.print("[bold red]Error:[/bold red] Input cannot be empty.")

    processed_input = raw_input.replace(',', '.')
    try:
        base_val = ast.literal_eval(processed_input)
    except:
        base_val = raw_input

    is_hashable = True
    try: hash(base_val)
    except: is_hashable = False
        
    is_numeric = False
    try:
        float(base_val)
        is_numeric = True
    except: pass

    # Estruturas de comparação
    comparisons = [
        ("String", str(base_val)),
        ("Integer", int(float(base_val)) if is_numeric else None),
        ("Float", float(base_val) if is_numeric else None),
        ("Array (C-style)", array.array('d', [float(base_val)]) if is_numeric else None),
        ("List", [base_val]),
        ("Tuple", (base_val,)),
        ("Set", {base_val} if is_hashable else None),
        ("Dict (Key)", {base_val: " "} if is_hashable else None),
        ("Dict (Val)", {" ": base_val})
    ]

    table = Table(border_style=THEME_COLOR, header_style=f"bold {THEME_COLOR}")
    table.add_column("STRUCTURE", style="bold white", width=18)
    table.add_column("CONTENT", style="italic", width=20)
    table.add_column("SHALLOW", justify="right", width=12)
    table.add_column("DEEP", justify="right", width=12)

    for name, obj in comparisons:
        if obj is not None:
            s_size, d_size = sys.getsizeof(obj), asizeof.asizeof(obj)
            display = str(obj) if len(str(obj)) < 20 else str(obj)[:17] + "..."
            size_style = "green" if d_size < 100 else ("yellow" if d_size < 500 else "red")
            table.add_row(name, display, f"[{size_style}]{s_size} B[/{size_style}]", f"[{size_style}]{d_size} B[/{size_style}]")
        else:
            table.add_row(name, f"[dim]N/A[/dim]", "[dim]-[/dim]", "[dim]-[/dim]", style="dim")
    
    console.print(table)
    
    explanation = "\n[bold yellow]TECHNICAL INSIGHT:[/bold yellow]\n • [bold cyan]SHALLOW[/bold cyan] container size.\n • [bold cyan]DEEP[/bold cyan] nested content size."
    console.print(explanation)
    
    if Prompt.ask(f"\n[bold yellow]Simulate 2.5 MILLION items of this type?[/bold yellow]", choices=["y", "n"], default="y") == "y":
        if isinstance(base_val, int): run_benchmark("1", base_val)
        elif isinstance(base_val, float): run_benchmark("2", base_val)
        else: run_benchmark("3", base_val)
    
    if Prompt.ask(f"\n[bold white]Analyze another value?[/bold white]", choices=["y", "n"], default="y") == "n":
        console.print(f"\n[italic magenta]Exiting system...[/italic magenta]\n")
        sys.exit()

def main():
    narrative = (
        "[bold italic cyan]\"Different data types occupy different amounts of memory.\n"
        "Every extra byte impacts performance and infrastructure costs.\n"
        "This lab measures real-world memory consumption in practice.\"[/bold italic cyan]"
    )

    while True:
        show_header("TECHNICAL MEMORY INSPECTION")
        console.print(get_system_info())
        console.print(f"\n{narrative}")
        run_inspector()

if __name__ == "__main__":
    main()