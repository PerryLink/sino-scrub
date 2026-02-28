"""文本清洗核心引擎"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from flashtext import KeywordProcessor

from .utils import load_dict, get_builtin_dict_path


class TextScrubber:
    """文本清洗器

    基于 FlashText 算法实现 O(N) 复杂度的关键词替换
    """

    def __init__(
        self,
        custom_dict_path: Optional[str] = None,
        categories: Optional[List[str]] = None
    ):
        """初始化文本清洗器

        Args:
            custom_dict_path: 自定义词库路径
            categories: 要加载的内置词库类别列表
                       可选值: ['translation', 'cultural', 'political']
                       默认加载所有类别
        """
        self.processor = KeywordProcessor(case_sensitive=False)
        self.metadata: Dict[str, Dict[str, Any]] = {}

        # 默认加载所有类别
        if categories is None:
            categories = ['translation', 'cultural', 'political']

        # 加载内置词库
        for category in categories:
            try:
                dict_path = get_builtin_dict_path(category)
                self._load_dict(dict_path)
            except Exception as e:
                raise RuntimeError(f"加载内置词库 '{category}' 失败: {e}")

        # 加载自定义词库
        if custom_dict_path:
            try:
                self._load_dict(Path(custom_dict_path))
            except FileNotFoundError:
                import warnings
                warnings.warn(f"自定义词库未找到: {custom_dict_path}")
            except Exception as e:
                raise RuntimeError(f"加载自定义词库失败: {e}")

    def _load_dict(self, path: Path) -> None:
        """加载词库文件

        Args:
            path: 词库文件路径
        """
        data = load_dict(path)

        for keyword, value in data.items():
            if isinstance(value, str):
                # 简单格式: {"keyword": "replacement"}
                self.processor.add_keyword(keyword, value)
                self.metadata[keyword] = {
                    'replacement': value,
                    'reason': None,
                    'category': None
                }
            elif isinstance(value, dict):
                # 富格式: {"keyword": {"replacement": "...", "reason": "...", "category": "..."}}
                replacement = value['replacement']
                self.processor.add_keyword(keyword, replacement)
                self.metadata[keyword] = {
                    'replacement': replacement,
                    'reason': value.get('reason'),
                    'category': value.get('category')
                }

    def scrub(
        self,
        text: str,
        track_changes: bool = False
    ) -> Tuple[str, Optional[List[Dict[str, Any]]]]:
        """清洗文本

        Args:
            text: 待清洗的文本
            track_changes: 是否追踪变更（用于 Debug Mode）

        Returns:
            如果 track_changes=False: (清洗后文本, None)
            如果 track_changes=True: (清洗后文本, 变更列表)

            变更列表格式:
            [
                {
                    'keyword': '原词',
                    'replacement': '替换词',
                    'reason': '替换原因',
                    'category': '类别',
                    'start': 起始位置,
                    'end': 结束位置
                },
                ...
            ]
        """
        if not track_changes:
            return self.processor.replace_keywords(text), None

        # 追踪变更
        changes = []
        keywords_found = self.processor.extract_keywords(text, span_info=True)

        for keyword, start, end in keywords_found:
            meta = self.metadata.get(keyword, {})
            changes.append({
                'keyword': keyword,
                'replacement': meta.get('replacement', ''),
                'reason': meta.get('reason'),
                'category': meta.get('category'),
                'start': start,
                'end': end
            })

        scrubbed_text = self.processor.replace_keywords(text)
        return scrubbed_text, changes
