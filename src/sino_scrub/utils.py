"""工具函数"""

import json
from pathlib import Path
from typing import Dict, Any


def load_dict(path: Path) -> Dict[str, Any]:
    """加载词库文件

    Args:
        path: 词库文件路径

    Returns:
        词库字典

    Raises:
        FileNotFoundError: 文件不存在
        json.JSONDecodeError: JSON 格式错误
    """
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_builtin_dict_path(category: str) -> Path:
    """获取内置词库路径

    Args:
        category: 词库类别 (translation, cultural, political)

    Returns:
        词库文件路径
    """
    data_dir = Path(__file__).parent / 'data'
    mapping = {
        'translation': 'translation_fix.json',
        'cultural': 'cultural_taboo.json',
        'political': 'political_sensitive.json'
    }
    return data_dir / mapping[category]
