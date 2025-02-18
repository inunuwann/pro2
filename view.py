from rich.console import Console
from rich.table import Table

console = Console()

def display_game_screen():
    console.print("               | 手札 (CPU) |", style="bold red")
    console.print("      [??]  [??]  [??]  [??]  [??]  [??]  [??]  [??]\n")

    console.print("               | 出来札 (CPU) |", style="bold red")
    console.print("      [菊に盃 (9月 盃)]   [柳に小野道風 (11月 光)]\n")

    console.print("                    | 役 |", style="bold yellow")
    console.print("               [月見で一杯] (5点)\n")

    console.print("--------------------------------------------------------------")

    console.print("                     | 場札 |", style="bold blue")
    table = Table(box=None)
    table.add_row("[梅に鶯 (2月 短冊)]", "[桜に幕 (3月 短冊)]", "[柳に小野道風 (11月 光)]")
    table.add_row("[菊に盃 (9月 盃)]", "[松に鶴 (1月 光)]", "[紅葉に鹿 (10月 たんざく)]")
    console.print(table)

    console.print("--------------------------------------------------------------")

    console.print("                    | 役 |", style="bold yellow")
    console.print("               [月見で一杯] (5点)\n")

    console.print("                    | 出来札 |", style="bold red")
    console.print("      [菊に盃 (9月 盃)]   [柳に小野道風 (11月 光)]\n")

    console.print("                 | 手札 (プレイヤー) |", style="bold green")
    table_player = Table(box=None)
    table_player.add_row("[柳に小野道風 (11月 光)]", "[萩に猪 (7月 たんざく)]", "[桜に幕 (3月 短冊)]")
    table_player.add_row("[藤に時鳥 (4月 短冊)]", "[松に鶴 (1月 光)]", "[菊に盃 (9月 盃)]")
    console.print(table_player)

# 画面を表示
display_game_screen()
