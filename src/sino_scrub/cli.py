"""命令行接口"""

from pathlib import Path
from typing import Optional, List
import typer
from typing_extensions import Annotated

from .processor import TextScrubber
from .visualizer import DiffVisualizer

app = typer.Typer(help="sino-scrub: 毫秒级清洗 AI 文本中的文化禁忌与敏感词")


@app.command()
def main(
    text_or_file: Annotated[str, typer.Argument(help="要清洗的文本内容或文件路径")],
    custom_dict: Annotated[Optional[str], typer.Option("--custom-dict", "-d", help="自定义词库路径")] = None,
    diff: Annotated[bool, typer.Option("--diff", help="显示替换前后对比")] = False,
    debug: Annotated[bool, typer.Option("--debug", help="Debug Mode，显示替换原因")] = False,
    category: Annotated[Optional[List[str]], typer.Option("--category", "-c", help="指定加载的词库类别")] = None,
    output: Annotated[Optional[str], typer.Option("--output", "-o", help="输出到文件")] = None,
):
    """清洗文本中的文化禁忌与敏感词"""

    # 判断是文件还是文本
    input_path = Path(text_or_file)
    if input_path.exists() and input_path.is_file():
        # 读取文件
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        # 直接使用文本
        text = text_or_file

    # 初始化清洗器
    try:
        scrubber = TextScrubber(
            custom_dict_path=custom_dict,
            categories=category
        )
    except Exception as e:
        typer.echo(f"错误: {e}", err=True)
        raise typer.Exit(1)

    # 清洗文本
    track_changes = diff or debug
    scrubbed_text, changes = scrubber.scrub(text, track_changes=track_changes)

    # 输出结果
    visualizer = DiffVisualizer()

    if diff or debug:
        visualizer.show_diff(text, scrubbed_text, changes if debug else None)
    else:
        visualizer.show_simple(scrubbed_text)

    # 保存到文件
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(scrubbed_text)
        typer.echo(f"\n已保存到: {output}")


if __name__ == "__main__":
    app()
