from notion_client import AsyncClient
import asyncio
import re
from typing import List, Dict, Set
from datetime import datetime
import argparse

NOTION_TOKEN = "your_integration_token"
notion = AsyncClient(auth=NOTION_TOKEN)


class NotionFormatter:
    def __init__(self):
        self.blocks_to_update: List[Dict] = []
        self.processed_blocks: Set[str] = set()
        self.total_blocks = 0
        self.processed_count = 0
        self.failed_blocks: List[Dict] = []

    def format_text(self, text: str) -> str:
        """Add spaces between Chinese and English/numbers"""
        text = re.sub(r"([\u4e00-\u9fa5])([A-Za-z0-9])", r"\1 \2", text)
        text = re.sub(r"([A-Za-z0-9])([\u4e00-\u9fa5])", r"\1 \2", text)
        return text

    def process_rich_text(self, rich_text: List[Dict]) -> tuple[List[Dict], bool]:
        """Process rich text content and return if modified"""
        modified = False
        if isinstance(rich_text, list):
            for item in rich_text:
                if "text" in item and "content" in item["text"]:
                    new_content = self.format_text(item["text"]["content"])
                    if new_content != item["text"]["content"]:
                        item["text"]["content"] = new_content
                        modified = True
        return rich_text, modified

    async def format_page_title(self, page_id: str):
        """Format the page title"""
        try:
            page = await notion.pages.retrieve(page_id)

            title_property = None
            if "properties" in page:
                # Find the title property (could be 'title' or 'Name', etc.)
                for prop_name, prop_value in page["properties"].items():
                    if prop_value["type"] in ["title"]:
                        title_property = prop_name
                        break

            if title_property:
                title = page["properties"][title_property]["title"]
                updated_title, modified = self.process_rich_text(title)

                if modified:
                    try:
                        await notion.pages.update(
                            page_id=page_id,
                            properties={title_property: {"title": updated_title}},
                        )
                        print("Page title updated")
                    except Exception as e:
                        print(f"Error updating page title: {str(e)}")

        except Exception as e:
            print(f"Error retrieving page title: {str(e)}")

    async def collect_blocks(self, block_id: str, level: int = 0):
        """Collect blocks that need formatting"""
        if block_id in self.processed_blocks:
            return
        self.processed_blocks.add(block_id)

        try:
            block = await notion.blocks.retrieve(block_id)
            self.total_blocks += 1
            self.processed_count += 1

            if self.processed_count % 10 == 0:
                print(f"Processing block {self.processed_count}...")

            block_type = block["type"]

            # Supported block types
            supported_types = [
                "paragraph",
                "heading_1",
                "heading_2",
                "heading_3",
                "bulleted_list_item",
                "numbered_list_item",
                "toggle",
                "quote",
                "callout",
                "to_do",
                "template",
                "synced_block",
                "breadcrumb",
                "table_of_contents",
                "link_to_page",
                "table_row",
                "column_list",
                "column",
            ]

            if block_type in supported_types:
                if block_type in block and "rich_text" in block[block_type]:
                    content = block[block_type]["rich_text"]
                    updated_content, modified = self.process_rich_text(content)
                    if modified:
                        self.blocks_to_update.append(
                            {
                                "block_id": block_id,
                                "block_type": block_type,
                                "content": updated_content,
                                "last_edited_time": block.get("last_edited_time", ""),
                            }
                        )

            try:
                children = await notion.blocks.children.list(block_id)
                tasks = [
                    self.collect_blocks(child["id"], level + 1)
                    for child in children["results"]
                ]
                await asyncio.gather(*tasks)
            except Exception as e:
                print(f"Error getting child blocks (block_id: {block_id}): {str(e)}")

        except Exception as e:
            print(f"Error processing block (block_id: {block_id}): {str(e)}")

    async def update_single_block(self, block: Dict, retry_count: int = 3):
        """Update a single block with retry mechanism"""
        for attempt in range(retry_count):
            try:
                # Get the latest block state
                current_block = await notion.blocks.retrieve(block["block_id"])

                # Check if the block has been modified
                if (
                    current_block.get("last_edited_time", "")
                    != block["last_edited_time"]
                ):
                    content = current_block[block["block_type"]]["rich_text"]
                    updated_content, modified = self.process_rich_text(content)
                    if not modified:
                        return True
                    block["content"] = updated_content

                await notion.blocks.update(
                    block_id=block["block_id"],
                    **{block["block_type"]: {"rich_text": block["content"]}},
                )
                return True

            except Exception as e:
                if attempt < retry_count - 1:
                    wait_time = (attempt + 1) * 0.5
                    print(
                        f"Failed to update block {block['block_id']}, retry in {wait_time}s: {str(e)}"
                    )
                    await asyncio.sleep(wait_time)
                else:
                    print(
                        f"Failed to update block {block['block_id']} after all attempts: {str(e)}"
                    )
                    return False

    async def update_blocks(self, batch_size: int = 3):
        """Update collected blocks in batches"""
        total = len(self.blocks_to_update)
        print(f"\nStarting to update {total} blocks...")

        for i in range(0, total, batch_size):
            batch = self.blocks_to_update[i : i + batch_size]

            results = await asyncio.gather(
                *[self.update_single_block(block) for block in batch],
                return_exceptions=False,
            )

            failed_blocks = [
                block for block, success in zip(batch, results) if not success
            ]
            self.failed_blocks.extend(failed_blocks)

            print(f"Processed {min(i + batch_size, total)}/{total} blocks")
            await asyncio.sleep(0.5)

        success_count = total - len(self.failed_blocks)
        print(f"\nUpdate completed:")
        print(f"- Success: {success_count}/{total}")
        if self.failed_blocks:
            print(f"- Failed: {len(self.failed_blocks)}/{total}")


async def format_notion_page(page_id: str):
    formatter = NotionFormatter()

    start_time = datetime.now()
    print(f"Starting formatting... ({start_time})")

    # Format page title first
    print("Formatting page title...")
    await formatter.format_page_title(page_id)

    # Then format page content
    print("\nCollecting blocks to update...")
    await formatter.collect_blocks(page_id)

    print(f"\nScan completed:")
    print(f"- Total blocks scanned: {formatter.total_blocks}")
    print(f"- Blocks to update: {len(formatter.blocks_to_update)}")

    if formatter.blocks_to_update:
        await formatter.update_blocks()

        # Handle failed blocks
        if formatter.failed_blocks:
            print("\nRetry failed blocks? (y/n)")
            if input().lower() == "y":
                formatter.blocks_to_update = formatter.failed_blocks
                formatter.failed_blocks = []
                await formatter.update_blocks()

    end_time = datetime.now()
    duration = end_time - start_time
    print(f"\nProcess completed! Total time: {duration}")


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Format spaces between Chinese and English in Notion documents"
    )
    parser.add_argument("page_id", help="Notion page ID to process")
    return parser.parse_args()


async def main():
    args = parse_args()
    await format_notion_page(args.page_id)


if __name__ == "__main__":
    asyncio.run(main())
