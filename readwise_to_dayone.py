#!/usr/bin/env python3

import os
import requests
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

class ReadwiseToDayOne:
    def __init__(self):
        load_dotenv()
        self.readwise_token = os.getenv('READWISE_TOKEN')
        self.journal_path = os.getenv('DAYONE_JOURNAL_PATH')
        
        # Define tag to emoji mapping
        self.tag_emoji_map = {
            'inspiration': '💡 Inspiration',
            'ai': '🤖 AI',
            'insight': '🤔 Insight'
        }
        
        if not self.readwise_token:
            raise ValueError("READWISE_TOKEN not found in environment variables")

    def format_tag(self, tag):
        """Format a tag with its corresponding emoji"""
        if isinstance(tag, dict):
            tag_name = tag.get('name', '').lower()
        else:
            tag_name = str(tag).lower()
            
        return self.tag_emoji_map.get(tag_name, f"❓ {tag_name.title()}")

    def get_todays_highlights(self):
        """Fetch today's highlights from Readwise using the export endpoint"""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        start = f"{today}T00:00:00Z"
        end = f"{today}T23:59:59Z"

        # Request the export
        export_params = {
            "updatedAfter": start,
            "updatedBefore": end
        }

        response = requests.get(
            "https://readwise.io/api/v2/export/",
            headers={"Authorization": f"Token {self.readwise_token}"},
            params=export_params
        )

        if response.status_code != 200:
            raise Exception(f"Failed to request export: {response.text}")

        return response.json()

    def download_image(self, url, book_title):
        """Download an image from URL and save it temporarily"""
        if not url:
            return None
            
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Create a temporary directory if it doesn't exist
                temp_dir = Path("/tmp/readwise_images")
                temp_dir.mkdir(parents=True, exist_ok=True)
                
                # Create a safe filename from the book title, replacing spaces with underscores
                safe_title = "".join(x if x.isalnum() or x == '_' else '_' for x in book_title).rstrip('_')
                image_path = temp_dir / f"{safe_title}.jpg"
                
                # Save the image
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                return str(image_path)
        except Exception as e:
            print(f"Failed to download image: {e}")
        return None

    def create_dayone_entry(self, content, image_path=None):
        """Create a new Day One entry using the CLI"""
        # Start with dayone2
        cmd = ["dayone2"]
        
        # Add journal if specified
        if self.journal_path:
            cmd.extend(["-j", self.journal_path])

        # Add image if available using attachments
        if image_path:
            cmd.extend(["-a", image_path, "--"])

        # Add the new command
        cmd.append("new")

        try:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(input=content)

            if process.returncode != 0:
                raise Exception(f"Failed to create Day One entry: {stderr}")

            return stdout
        except FileNotFoundError:
            raise Exception("Day One CLI not found. Please install it first.")
        finally:
            # Clean up temporary image if it exists
            if image_path and Path(image_path).exists():
                Path(image_path).unlink()

    def format_highlights(self, export_data):
        """Format highlights from export data into a nice markdown structure"""
        if not export_data or not export_data.get('results'):
            return "No highlights for today."

        formatted_text = ""
        
        # Process each book/article in the results
        for book in export_data['results']:
            # Download the cover image if available
            image_path = None
            if book.get("cover_image_url"):
                image_path = self.download_image(book["cover_image_url"], book["title"])
            
            # Add title as main heading
            formatted_text += f"# {book['title']}\n\n"
            
            # Add metadata section
            formatted_text += "## Metadata\n\n"
            if book.get("author"):
                formatted_text += f"Author: {book['author']}\n"
            if book.get("category"):
                formatted_text += f"Category: {book['category']}\n"
            if book.get("source"):
                formatted_text += f"Source: {book['source']}\n"
            if book.get("source_url"):
                formatted_text += f"URL: {book['source_url']}\n"
            if book.get("summary"):
                formatted_text += f"\nSummary: {book['summary']}\n"
            formatted_text += "\n"

            # Add cover image placeholder if available
            if image_path:
                formatted_text += "Cover Image:\n[{attachment}]\n\n"

            # Add highlights section
            formatted_text += "## Highlights\n\n"
            for highlight in book.get('highlights', []):
                # Add the highlight text
                formatted_text += f"> {highlight['text']}\n\n"
                
                # Add tags if they exist with emojis
                if highlight.get('tags'):
                    tags = [self.format_tag(tag) for tag in highlight['tags']]
                    formatted_text += f"Tags: {' '.join(tags)}\n\n"
                
                # Add note if exists
                if highlight.get('note'):
                    formatted_text += f"Note: {highlight['note']}\n\n"

            # Create the entry with the downloaded image
            self.create_dayone_entry(formatted_text, image_path)
            formatted_text = ""  # Reset for next book/article

        return "Successfully created entries for all highlights!"

    def run(self):
        """Main execution method"""
        try:
            export_data = self.get_todays_highlights()
            result = self.format_highlights(export_data)
            print(result)
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    app = ReadwiseToDayOne()
    app.run() 