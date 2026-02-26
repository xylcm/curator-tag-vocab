"""
导出服务 - 数据导出业务逻辑
"""
import csv
import json
import tempfile
from datetime import datetime
from typing import List, Dict, Any, Tuple
from src.models import Tag
from src.dao import TagDAO
from src.services.category_service import CategoryService


class ExportService:
    """导出业务服务"""

    def __init__(self, tag_dao: TagDAO, category_service: CategoryService):
        self.tag_dao = tag_dao
        self.category_service = category_service

    def _get_export_tags(self) -> List[Tag]:
        """获取需要导出的标签（去重、排序）"""
        return self.tag_dao.get_unique_active_tags()

    def export_to_protobuf(self) -> Tuple[bytes, str]:
        """
        导出为 Protobuf 格式
        返回: (二进制数据, 文件名)
        """
        from src.protobuf import tags_vocabulary_pb2

        tags = self._get_export_tags()
        categories = self.category_service.get_all_categories()

        # 创建 protobuf 对象
        vocab = tags_vocabulary_pb2.TagVocabulary()
        version = datetime.now().strftime("%Y%m%d_%H%M%S")
        vocab.version = version
        vocab.modified_time = datetime.now().isoformat()

        # 添加标签
        for tag_data in tags:
            tag_msg = vocab.tags.add()
            tag_msg.name = tag_data.tag
            tag_msg.context = tag_data.context
            tag_msg.category = tag_data.category

            # 添加翻译
            if tag_data.translations.zh_CN:
                trans_msg = tag_msg.translations.add()
                trans_msg.lang = 'zh_CN'
                trans_msg.text = tag_data.translations.zh_CN
            if tag_data.translations.en:
                trans_msg = tag_msg.translations.add()
                trans_msg.lang = 'en'
                trans_msg.text = tag_data.translations.en

        vocab.vocab_size = len(tags)

        # 添加分类信息
        for i, category in enumerate(categories, 1):
            category_msg = vocab.categories.add()
            category_msg.id = category.id
            category_msg.order = i
            category_msg.name = category.category
            category_msg.available = category.available

            for lang_code, translation_text in category.translations.items():
                trans_msg = category_msg.translations.add()
                trans_msg.lang = lang_code
                trans_msg.text = translation_text

        filename = f"tags_vocabulary_{version}.pb"
        return vocab.SerializeToString(), filename

    def export_to_csv(self) -> Tuple[str, str]:
        """
        导出为 CSV 格式
        返回: (CSV内容, 文件名)
        """
        tags = self._get_export_tags()

        # 构建 CSV 内容
        lines = ['en\tzh_CN\tcategory']

        for tag_data in tags:
            zh_translation = tag_data.translations.zh_CN or ''
            en_translation = tag_data.tag
            category = tag_data.category

            # 使用制表符分隔，处理特殊字符
            lines.append(f"{en_translation}\t{zh_translation}\t{category}")

        csv_content = '\n'.join(lines)
        filename = f"tags_vocabulary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        return csv_content, filename

    def export_to_dict(self) -> Dict[str, Any]:
        """导出为字典格式（用于API）"""
        tags = self._get_export_tags()
        categories = self.category_service.get_all_categories()

        return {
            'version': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'modified_time': datetime.now().isoformat(),
            'vocab_size': len(tags),
            'tags': [
                {
                    'name': tag.tag,
                    'context': tag.context,
                    'category': tag.category,
                    'translations': tag.translations.to_dict()
                }
                for tag in tags
            ],
            'categories': [
                {
                    'id': cat.id,
                    'name': cat.category,
                    'available': cat.available,
                    'translations': cat.translations
                }
                for cat in categories
            ]
        }
