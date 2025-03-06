from functools import total_ordering

# Constants
B = 1
KB = B * 1024
MB = KB * 1024
GB = MB * 1024
TB = GB * 1024

units = [
    (B, ['B', 'b', 'byte', 'Byte']),
    (KB, ['K', 'KB', 'KiB', 'kilobyte', 'Kilobyte']),
    (MB, ['M', 'MB', 'MiB', 'megabyte', 'Megabyte']),
    (GB, ['G', 'GB', 'GiB', 'gigabyte', 'Gigabyte']),
    (TB, ['T', 'TB', 'TiB', 'terabyte', 'Terabyte']),
]

suffixes = {}
for value, names in units:
    for name in names:
        suffixes[name] = value

# Exceptions
class InvalidSuffixError(Exception):
    def __init__(self, error_suffix, suffixes):
        self.error_suffix = error_suffix
        self.suffixes = suffixes

    def __str__(self):
        return f"Invalid suffix: {self.error_suffix}. Acceptable suffixes: {', '.join(self.suffixes)}"

class MissingNumericPartError(Exception):
    def __str__(self):
        return 'Numeric part is missing'

class NotDivisibleByBlock(Exception):
    def __init__(self, bytes_value, block_size):
        self.bytes_value = bytes_value
        self.block_size = block_size

    def __str__(self):
        return f"Specified size {self.bytes_value} is not divisible by block size {self.block_size}"

# Functions
def parse_numeric_string(numeric_string: str):
    """
    Parses a string containing a number with suffix.

    :param numeric_string: Input string in "number+suffix" format (e.g., "11222KB")
    :return: Tuple (numeric_part, suffix_part)
    :raises MissingNumericPartError: If no numeric part found
    :raises InvalidSuffixError: If invalid suffix is used
    """
    numeric_part = ''
    suffix_part = ''

    for i, char in enumerate(numeric_string):
        if char.isdigit():
            numeric_part += char
        else:
            suffix_part = numeric_string[i:]
            break

    if not numeric_part:
        raise MissingNumericPartError()

    if suffix_part:
        if suffix_part not in suffixes:
            raise InvalidSuffixError(suffix_part, suffixes.keys())
    else:
        suffix_part = 'B'

    return int(numeric_part), suffix_part

@total_ordering
class ByteSize:
    def __init__(self, size_str: str):
        if size_str.startswith("0x"):  # Hexadecimal format
            self.size_in_bytes = int(size_str, 16)
            self.default_suffix = 'B'
        else:  # Format with suffixes or plain bytes
            value, suffix = parse_numeric_string(size_str)
            self.size_in_bytes = value * suffixes[suffix]
            self.default_suffix = suffix

    def to_kib(self) -> str:
        """Convert to kibibytes (KiB)"""
        if self.size_in_bytes == 0:
            return "0"
        value = self.size_in_bytes / KB
        return f"{int(value)}KB" if value.is_integer() else f"{value:.2f}KB"

    def to_mib(self) -> str:
        """Convert to mebibytes (MiB)"""
        if self.size_in_bytes == 0:
            return "0"
        value = self.size_in_bytes / MB
        return f"{int(value)}MB" if value.is_integer() else f"{value:.2f}MB"

    def to_gib(self) -> str:
        """Convert to gibibytes (GiB)"""
        if self.size_in_bytes == 0:
            return "0"
        value = self.size_in_bytes / GB
        return f"{int(value)}GB" if value.is_integer() else f"{value:.2f}GB"

    def to_tib(self) -> str:
        """Convert to tebibytes (TiB)"""
        if self.size_in_bytes == 0:
            return "0"
        value = self.size_in_bytes / TB
        return f"{int(value)}TB" if value.is_integer() else f"{value:.2f}TB"

    def to_bytes(self) -> str:
        """Convert to bytes (B)"""
        return f"{self.size_in_bytes}B"

    def raw_val(self) -> int:
        """Get raw byte value as integer"""
        return self.size_in_bytes

    def to_default(self) -> str:
        """Convert using the original input suffix"""
        if self.size_in_bytes == 0:
            return "0"
        value = self.size_in_bytes / suffixes[self.default_suffix]
        return f"{int(value)}{self.default_suffix}" if value.is_integer() else f"{value:.2f}{self.default_suffix}"

    def to_closest_readable(self, external_units: list = ['B', 'KB', 'MB', 'GB', 'TB']):
        """
        Convert to human-readable format using the most appropriate unit

        :param external_units: List of units to consider for conversion
        :return: Formatted string like '512 KB', '2.5 MB', etc.
        """
        if not self.size_in_bytes:
            return '0'
        size = self.size_in_bytes
        unit_index = 0

        while size >= 1024 and unit_index < len(external_units) - 1:
            size /= 1024
            unit_index += 1

        readable_size = f"{size:.2f}".rstrip('0').rstrip('.')
        return f"{readable_size}{external_units[unit_index]}"

    def is_divisible_by_block(self, block_size: int):
        """Check if size is divisible by block size"""
        return block_size != 0 and self.size_in_bytes % block_size == 0

    def __str__(self):
        return self.to_bytes()

    def __eq__(self, other):
        if isinstance(other, ByteSize):
            return self.size_in_bytes == other.size_in_bytes
        elif isinstance(other, (int, float)):
            return self.size_in_bytes == other
        elif isinstance(other, str):
            if other.startswith("0x"):
                return self.size_in_bytes == int(other, 16)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, ByteSize):
            return self.size_in_bytes < other.size_in_bytes
        elif isinstance(other, (int, float)):
            return self.size_in_bytes < other
        elif isinstance(other, str):
            if other.startswith("0x"):
                return self.size_in_bytes < int(other, 16)
        return NotImplemented