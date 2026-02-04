"""
Export the vocabulary to protobuf format.
"""
import os
import json
from datetime import datetime

from src.db import VocabDB
from src.protobuf import tags_vocabulary_pb2
import argparse

parser = argparse.ArgumentParser(description='Export the vocabulary to protobuf format.')
parser.add_argument("--output-file", '-o', type=str, default="outputs/tags_vocabulary.pb", help='Output file path')
args = parser.parse_args()


class VocabularyExporter:

    def load_uniq_tags(self):
        db = VocabDB()
        tags = db.query("SELECT * FROM tags_vocab WHERE is_deleted = 0 AND available = 1")
        
        seen_tags = set()
        unique_tags = []
        for tag in tags:
            if tag['tag'] not in seen_tags:
                seen_tags.add(tag['tag'])
                unique_tags.append(tag)
            else:
                print(f"Duplicate tag: {tag['tag']}")
        
        unique_tags = sorted(unique_tags, key=lambda x: x['tag'])
        return unique_tags


    def export_protobuf(self, output_file: str = None, version: str = None):

        if output_file is None:
            output_file = os.path.join("outputs", "tags_vocabulary.pb")
        if version is None:
            version = datetime.now().strftime("%Y%m%d_%H%M%S")

        if not os.path.exists(os.path.dirname(output_file)):
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        unique_tags = self.load_uniq_tags()

        print(f"Total unique tags: {len(unique_tags)}")
        
        vocab = tags_vocabulary_pb2.TagVocabulary()
        vocab.version = version
        vocab.modified_time = datetime.now().isoformat()
        
        for tag_data in unique_tags:
            tag_msg = vocab.tags.add()
            tag_msg.name = tag_data['tag']
            tag_msg.context = tag_data.get('context') or ''
            tag_msg.category = tag_data.get('category') or ''
            
            translations = tag_data.get('translations', {})
            if translations:
                for lang_code, translation_text in translations.items():
                    trans_msg = tag_msg.translations.add()
                    trans_msg.lang = lang_code
                    trans_msg.text = translation_text

        vocab.vocab_size = len(unique_tags)

        categories_file = os.path.join("config", "categories.json")
        with open(categories_file, 'r') as f:
            categories = json.load(f)
            for i, category in enumerate(categories, 1):
                category_msg = vocab.categories.add()
                category_msg.id = category['id']
                category_msg.order = i
                category_msg.name = category['category']
                category_msg.available = category['available']
                for lang_code, translation_text in category['translations'].items():
                    trans_msg = category_msg.translations.add()
                    trans_msg.lang = lang_code
                    trans_msg.text = translation_text
        
        with open(output_file, 'wb') as f:
            f.write(vocab.SerializeToString())
        
        print(f"Exported {len(unique_tags)} tags to {output_file}. Version: {vocab.version}, File size: {os.path.getsize(output_file)} bytes")
        return vocab


    def export_csv(self, output_file: str = None):
        if output_file is None:
            output_file = os.path.join("outputs", "tags_vocabulary.csv")
        
        unique_tags = self.load_uniq_tags()
        
        with open(output_file, 'w') as f:
            f.write('en\tzh_CN\tcategory\n')
            for tag_data in unique_tags:
                tag_cn = tag_data.get('translations', {}).get('zh_CN', '')
                tag_en = tag_data['tag']
                category = tag_data.get('category', '')
                f.write(f"{tag_en}\t{tag_cn}\t{category}\n")
        
        print(f"Exported {len(unique_tags)} tags to {output_file}")
        return output_file

    def verify_protobuf(self, output_file: str = None) -> None:

        if output_file is None:
            output_file = os.path.join("outputs", "tags_vocabulary.pb")
        
        vocab = tags_vocabulary_pb2.TagVocabulary()
        with open(output_file, 'rb') as f:
            vocab.ParseFromString(f.read())
        
        print(f"Version: {vocab.version}. Last modified: {vocab.modified_time}, Total tags: {vocab.vocab_size}")
        
        print("\nFirst 5 tags:")
        for i, tag in enumerate(vocab.tags[:5]):
            print(f"  {i+1}. {tag.name}")
            if tag.context:
                print(f"     → {tag.context}")
            if tag.category:
                print(f"     → {tag.category}")
            if tag.translations:
                for trans in tag.translations:
                    print(f"     {trans.lang}: {trans.text}")

        print("\nFirst 5 categories:")
        for i, category in enumerate(vocab.categories[:5]):
            print(f"  {i+1}. {category.name}")
            print(f"     → {category.order}")
            if category.available:
                print(f"     → Available")
            else:
                print(f"     → Not available")
            if category.translations:
                for trans in category.translations:
                    print(f"     → {trans.lang}: {trans.text}")


def main():
    exporter = VocabularyExporter()
    pb_output_file = os.path.abspath(args.output_file)
    exporter.export_protobuf(output_file=pb_output_file)
    exporter.verify_protobuf(output_file=pb_output_file)
    exporter.export_csv(output_file=os.path.abspath(args.output_file.replace(".pb", ".csv")))

if __name__ == "__main__":
    main()