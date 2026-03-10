"""Export service for generating export files."""

import csv
import io
import tempfile
from datetime import datetime
from typing import Dict, List, Any, Tuple

from src.models.tag import Tag
from src.repositories.tag_repository import TagRepository
from src.services.category_service import CategoryService


class ExportService:
    """Service for exporting vocabulary data."""

    def __init__(
        self,
        tag_repository: TagRepository = None,
        category_service: CategoryService = None,
    ):
        self._tag_repo = tag_repository or TagRepository()
        self._category_service = category_service or CategoryService()

    def _get_unique_tags(self) -> List[Tag]:
        """Get unique, available, non-deleted tags."""
        tags = self._tag_repo.get_all_available()

        # Remove duplicates by tag name
        seen = set()
        unique_tags = []
        for tag in tags:
            if tag.tag not in seen:
                seen.add(tag.tag)
                unique_tags.append(tag)

        # Sort by tag name
        return sorted(unique_tags, key=lambda t: t.tag)

    def export_to_csv(self) -> Tuple[str, str]:
        """Export tags to CSV format.

        Returns:
            Tuple of (file_path, filename)
        """
        tags = self._get_unique_tags()

        # Create temp file
        temp_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", encoding="utf-8"
        )

        # Write CSV
        writer = csv.writer(temp_file, delimiter="\t")
        writer.writerow(["en", "zh_CN", "category"])

        for tag in tags:
            tag_cn = tag.translations.get("zh_CN", "") if tag.translations else ""
            writer.writerow([tag.tag, tag_cn, tag.category])

        temp_file.close()

        filename = f"tags_vocabulary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        return temp_file.name, filename

    def export_to_protobuf(self) -> Tuple[str, str]:
        """Export tags to Protobuf format.

        Returns:
            Tuple of (file_path, filename)
        """
        from src.protobuf import tags_vocabulary_pb2

        tags = self._get_unique_tags()
        categories = self._category_service.get_all()

        # Create protobuf object
        vocab = tags_vocabulary_pb2.TagVocabulary()
        vocab.version = datetime.now().strftime("%Y%m%d_%H%M%S")
        vocab.modified_time = datetime.now().isoformat()

        # Add tags
        for tag in tags:
            tag_msg = vocab.tags.add()
            tag_msg.name = tag.tag
            tag_msg.context = tag.context
            tag_msg.category = tag.category

            if tag.translations:
                for lang_code, translation_text in tag.translations.items():
                    trans_msg = tag_msg.translations.add()
                    trans_msg.lang = lang_code
                    trans_msg.text = translation_text

        vocab.vocab_size = len(tags)

        # Add categories
        for i, category in enumerate(categories, 1):
            category_msg = vocab.categories.add()
            category_msg.id = category["id"]
            category_msg.order = i
            category_msg.name = category["category"]
            category_msg.available = category["available"]

            translations = category.get("translations", {})
            for lang_code, translation_text in translations.items():
                trans_msg = category_msg.translations.add()
                trans_msg.lang = lang_code
                trans_msg.text = translation_text

        # Write to temp file
        temp_file = tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".pb")
        temp_file.write(vocab.SerializeToString())
        temp_file.close()

        filename = f"tags_vocabulary_{vocab.version}.pb"
        return temp_file.name, filename

    def get_export_data(self) -> Dict[str, Any]:
        """Get export data as dictionary."""
        tags = self._get_unique_tags()
        categories = self._category_service.get_all()

        return {
            "version": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "modified_time": datetime.now().isoformat(),
            "vocab_size": len(tags),
            "tags": [tag.to_dict() for tag in tags],
            "categories": categories,
        }
