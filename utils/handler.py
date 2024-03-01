import re
import xml.etree.ElementTree as etree

def get_page_range(page_range_str):
    """Validates a page range string with flexible formatting and returns the range.

    Args:
        page_range_str: The page range string (e.g., '1 - 10', ' 5, 12', '10').

    Returns:
        A tuple containing (start_page, end_page) if valid, otherwise None.

    Raises:
        ValueError: If the page range is invalid.
    """

    match = re.search(r"^\s*(\d+)\s*([-,\s]+\s*(\d+)\s*)?$", page_range_str)
    if match:
        start_page = int(match.group(1))
        end_page = int(match.group(3)) if match.group(3) else start_page  # Handle single page case

        if start_page <= end_page:
            return start_page, end_page
        else:
            raise ValueError("Invalid page range: start page must be less than or equal to end page.")
    else:
        raise ValueError("Invalid page range format.") 


def generate_chunks(total_count, chunk_size):
    """Generates start and end indices for breaking a count into chunks.

    Args:
        total_count: The total number of items.
        chunk_size: The desired size of each chunk.

    Yields:
        Tuples containing (start_index, end_index) for each chunk.
    """

    start_index = 1
    end_index = chunk_size

    while start_index <= total_count:
        yield start_index, end_index
        start_index += chunk_size
        end_index += chunk_size
        end_index = min(end_index, total_count)  # Handle last chunk 