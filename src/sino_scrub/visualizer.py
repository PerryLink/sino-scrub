"""终端可视化模块"""

from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


class DiffVisualizer:
    """差异可视化器

    使用 Rich 库显示文本清洗前后的对比
    """

    def __init__(self):
        self.console = Console()

    def show_diff(
        self,
        original: str,
        scrubbed: str,
        changes: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """显示文本清洗前后的对比

        Args:
            original: 原始文本
            scrubbed: 清洗后的文本
            changes: 变更列表（用于 Debug Mode）
        """
        # 创建对比表格
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("原文", style="red", width=50)
        table.add_column("清洗后", style="green", width=50)

        # 高亮显示变更
        if changes:
            original_text = Text(original)
            scrubbed_text = Text(scrubbed)

            # 标记原文中的敏感词
            for change in changes:
                keyword = change['keyword']
                # 在原文中查找并高亮
                start = original.find(keyword)
                if start != -1:
                    original_text.stylize("bold red on yellow", start, start + len(keyword))

            # 标记替换后的词
            for change in changes:
                replacement = change['replacement']
                # 在清洗后文本中查找并高亮
                start = scrubbed.find(replacement)
                if start != -1:
                    scrubbed_text.stylize("bold green on yellow", start, start + len(replacement))

            table.add_row(original_text, scrubbed_text)
        else:
            table.add_row(original, scrubbed)

        self.console.print(table)

        # 显示 Debug 信息
        if changes:
            self.console.print("\n[bold cyan]Debug Information:[/bold cyan]")
            for i, change in enumerate(changes, 1):
                self.console.print(f"\n  {i}. [red]'{change['keyword']}'[/red] → [green]'{change['replacement']}'[/green]")
                if change.get('category'):
                    self.console.print(f"     Category: [yellow][{change['category']}][/yellow]")
                if change.get('reason'):
                    self.console.print(f"     Reason: {change['reason']}")

    def show_simple(self, text: str) -> None:
        """简单显示清洗后的文本

        Args:
            text: 要显示的文本
        """
        self.console.print(text)
