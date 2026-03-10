"""
Export service for data export functionality.
"""

import csv
import io
import json
import logging
import os
import tempfile
from datetime import datetime
from typing import List, BinaryIO

from ..models.tag import Tag
from ..models.category import Category
from .tag_service import TagService
from .category_service import CategoryService

logger = logging.getLogger(__name__)


class ExportService:
    """Service for exporting tag vocabulary data."""

    def __init__(self, tag_service: TagService, category_service: CategoryService):
        self.tag_service = tag_service
        self.category_service = category_service

    def export_to_csv(self) -> str:
        """Export tags to CSV format. Returns file path."""
        tags = self.tag_service.get_unique_active_tags()

        # Create temp file
        temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            delete=False,
            suffix='.csv',
            encoding='utf-8'
        )

        writer = csv.writer(temp_file, delimiter='\t')
        writer.writerow(['en', 'zh_CN', 'category'])

        for tag in tags:
            zh_translation = tag.translations.get('zh_CN', '')
            writer.writerow([tag.tag, zh_translation, tag.category])

        temp_file.close()

        logger.info(f"Exported {len(tags)} tags to CSV: {temp_file.name}")
        return temp_file.name

    def export_to_protobuf(self) -> str:
        """Export tags to Protobuf binary format. Returns file path."""
        try:
            from ..protobuf import tags_vocabulary_pb2
        except ImportError:
            raise ImportError("Protobuf module not available")

        tags = self.tag_service.get_unique_active_tags()
        categories = self.category_service.get_all_categories()

        vocab = tags_vocabulary_pb2.TagVocabulary()
        vocab.version = datetime.now().strftime("%Y%m%d_%H%M%S")
        vocab.modified_time = datetime.now().isoformat()
        vocab.vocab_size = len(tags)

        # Add tags
        for tag in tags:
            tag_msg = vocab.tags.add()
            tag_msg.name = tag.tag
            tag_msg.context = tag.context or ''
            tag_msg.category = tag.category or ''

            for lang_code, translation_text in tag.translations.items():
                trans_msg = tag_msg.translations.add()
                trans_msg.lang = lang_code
                trans_msg.text = translation_text

        # Add categories
        for i, category in enumerate(categories, 1):
            cat_msg = vocab.categories.add()
            cat_msg.id = category.id
            cat_msg.order = i
            cat_msg.name = category.name
            cat_msg.available = category.available

            for lang_code, translation_text in category.translations.items():
                trans_msg = cat_msg.translations.add()
                trans_msg.lang = lang_code
                trans_msg.text = translation_text

        # Write to temp file
        temp_file = tempfile.NamedTemporaryFile(
            mode='wb',
            delete=False,
            suffix='.pb'
        )
        temp_file.write(vocab.SerializeToString())
        temp_file.close()

        logger.info(f"Exported {len(tags)} tags to Protobuf: {temp_file.name}")
        return temp_file.name

    def get_export_filename(self, extension: str) -> str:
        """Generate export filename with timestamp."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"tags_vocabulary_{timestamp}.{extension}"
