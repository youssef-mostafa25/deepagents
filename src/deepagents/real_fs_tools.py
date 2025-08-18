import os
import pathlib
import re
import subprocess
import shutil
import tempfile
from langchain_core.tools import tool
from typing import Annotated, Optional, Union

from deepagents.prompts import (
    EDIT_DESCRIPTION,
    TOOL_DESCRIPTION,
    GLOB_DESCRIPTION,
    GREP_DESCRIPTION,
    PATCH_DESCRIPTION,
)


def ls(path: str = ".") -> list[str]:
    """List all files in the specified directory."""
    try:
        path_obj = pathlib.Path(path)
        if not path_obj.exists():
            return [f"Error: Path '{path}' does not exist"]
        if not path_obj.is_dir():
            return [f"Error: Path '{path}' is not a directory"]

        # Get all files and directories in the path
        items = []
        for item in path_obj.iterdir():
            items.append(str(item.name))
        return sorted(items)
    except Exception as e:
        return [f"Error listing directory: {str(e)}"]


@tool(description=TOOL_DESCRIPTION)
def read_file(
    file_path: str,
    offset: int = 0,
    limit: int = 2000,
) -> str:
    """Read file from disk."""
    try:
        path_obj = pathlib.Path(file_path)

        # Check if file exists
        if not path_obj.exists():
            return f"Error: File '{file_path}' not found"

        if not path_obj.is_file():
            return f"Error: '{file_path}' is not a file"

        # Read file content
        try:
            with open(path_obj, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try reading as binary and decode with errors ignored
            with open(path_obj, "rb") as f:
                content = f.read().decode("utf-8", errors="ignore")

        # Handle empty file
        if not content or content.strip() == "":
            return "System reminder: File exists but has empty contents"

        # Split content into lines
        lines = content.splitlines()

        # Apply line offset and limit
        start_idx = offset
        end_idx = min(start_idx + limit, len(lines))

        # Handle case where offset is beyond file length
        if start_idx >= len(lines):
            return (
                f"Error: Line offset {offset} exceeds file length ({len(lines)} lines)"
            )

        # Format output with line numbers (cat -n format)
        result_lines = []
        for i in range(start_idx, end_idx):
            line_content = lines[i]

            # Truncate lines longer than 2000 characters
            if len(line_content) > 2000:
                line_content = line_content[:2000]

            # Line numbers start at 1, so add 1 to the index
            line_number = i + 1
            result_lines.append(f"{line_number:6d}\t{line_content}")

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def write_file(
    file_path: str,
    content: str,
) -> str:
    """Write content to a file on disk."""
    try:
        path_obj = pathlib.Path(file_path)

        # Create parent directories if they don't exist
        path_obj.parent.mkdir(parents=True, exist_ok=True)

        # Write content to file
        with open(path_obj, "w", encoding="utf-8") as f:
            f.write(content)

        return f"Successfully wrote to file '{file_path}'"

    except Exception as e:
        return f"Error writing file: {str(e)}"


@tool(description=EDIT_DESCRIPTION)
def edit_file(
    file_path: str,
    old_string: str,
    new_string: str,
    replace_all: bool = False,
) -> str:
    """Edit a file on disk by replacing old_string with new_string."""
    try:
        path_obj = pathlib.Path(file_path)

        # Check if file exists
        if not path_obj.exists():
            return f"Error: File '{file_path}' not found"

        if not path_obj.is_file():
            return f"Error: '{file_path}' is not a file"

        # Read current file content
        try:
            with open(path_obj, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            return f"Error: File '{file_path}' contains non-UTF-8 content"

        # Check if old_string exists in the file
        if old_string not in content:
            return f"Error: String not found in file: '{old_string}'"

        # If not replace_all, check for uniqueness
        if not replace_all:
            occurrences = content.count(old_string)
            if occurrences > 1:
                return f"Error: String '{old_string}' appears {occurrences} times in file. Use replace_all=True to replace all instances, or provide a more specific string with surrounding context."
            elif occurrences == 0:
                return f"Error: String not found in file: '{old_string}'"

        # Perform the replacement
        if replace_all:
            new_content = content.replace(old_string, new_string)
            replacement_count = content.count(old_string)
            result_msg = f"Successfully replaced {replacement_count} instance(s) of the string in '{file_path}'"
        else:
            new_content = content.replace(
                old_string, new_string, 1
            )  # Replace only first occurrence
            result_msg = f"Successfully replaced string in '{file_path}'"

        # Write the updated content back to the file
        with open(path_obj, "w", encoding="utf-8") as f:
            f.write(new_content)

        return result_msg

    except Exception as e:
        return f"Error editing file: {str(e)}"


@tool(description=GLOB_DESCRIPTION)
def glob(
    pattern: str,
    path: str = ".",
    max_results: int = 100,
    include_dirs: bool = False,
    recursive: bool = True,
) -> str:
    """Find files and directories using glob patterns."""
    try:
        path_obj = pathlib.Path(path)
        if not path_obj.exists():
            return f"Error: Path '{path}' does not exist"

        if not path_obj.is_dir():
            return f"Error: Path '{path}' is not a directory"

        results = []

        # Use pathlib.Path.glob or rglob based on recursive setting
        try:
            if recursive:
                # For recursive search, use rglob
                matches = path_obj.rglob(pattern)
            else:
                # For non-recursive search, use glob
                matches = path_obj.glob(pattern)

            # Process matches
            for match in matches:
                if len(results) >= max_results:
                    break

                # Check if we should include this result
                if match.is_file():
                    results.append(str(match))
                elif match.is_dir() and include_dirs:
                    results.append(f"{match}/")

            # Sort results for consistent output
            results.sort()

        except Exception as e:
            return f"Error processing glob pattern: {str(e)}"

        if not results:
            search_type = "recursive" if recursive else "non-recursive"
            dirs_note = " (including directories)" if include_dirs else ""
            return f"No matches found for pattern '{pattern}' in '{path}' ({search_type} search{dirs_note})"

        result_count = len(results)
        header = f"Found {result_count} matches for pattern '{pattern}'"
        if result_count >= max_results:
            header += f" (limited to {max_results} results)"
        header += ":\n\n"

        return header + "\n".join(results)

    except Exception as e:
        return f"Error in glob search: {str(e)}"


@tool(description=GREP_DESCRIPTION)
def grep(
    pattern: str,
    files: Optional[Union[str, list[str]]] = None,
    path: Optional[str] = None,
    file_pattern: str = "*",
    max_results: int = 50,
    case_sensitive: bool = False,
    context_lines: int = 0,
    regex: bool = False,
    recursive: bool = True,
) -> str:
    """Search for text patterns within files."""
    try:
        if not files and not path:
            return "Error: Must provide either 'files' parameter or 'path' parameter"

        # Prepare list of files to search
        files_to_search = []

        if files:
            # Convert single file to list
            if isinstance(files, str):
                files = [files]

            # Validate and add files
            for file_path in files:
                path_obj = pathlib.Path(file_path)
                if path_obj.exists() and path_obj.is_file():
                    files_to_search.append(path_obj)
                else:
                    return f"Error: File '{file_path}' does not exist or is not a file"

        elif path:
            # Search for files in directory using file_pattern
            path_obj = pathlib.Path(path)
            if not path_obj.exists():
                return f"Error: Path '{path}' does not exist"

            if not path_obj.is_dir():
                return f"Error: Path '{path}' is not a directory"

            # Find files matching the file pattern
            if recursive:
                matches = path_obj.rglob(file_pattern)
            else:
                matches = path_obj.glob(file_pattern)

            for match in matches:
                if match.is_file():
                    files_to_search.append(match)

        if not files_to_search:
            return f"No files found to search"

        # Prepare regex pattern
        if regex:
            try:
                flags = 0 if case_sensitive else re.IGNORECASE
                compiled_pattern = re.compile(pattern, flags)
            except re.error as e:
                return f"Error: Invalid regex pattern: {str(e)}"
        else:
            compiled_pattern = None

        results = []
        total_matches = 0

        for file_path in files_to_search:
            if total_matches >= max_results:
                break

            try:
                # Try to read file as text
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                except UnicodeDecodeError:
                    # Skip binary files
                    continue

                file_matches = []

                # Search through lines
                for line_num, line in enumerate(lines, 1):
                    line_content = line.rstrip("\n\r")
                    match_found = False

                    if regex:
                        match_found = compiled_pattern.search(line_content) is not None
                    else:
                        if case_sensitive:
                            match_found = pattern in line_content
                        else:
                            match_found = pattern.lower() in line_content.lower()

                    if match_found:
                        # Add context lines if requested
                        context_start = max(0, line_num - 1 - context_lines)
                        context_end = min(len(lines), line_num + context_lines)

                        match_info = {
                            "line_num": line_num,
                            "line_content": line_content,
                            "context_lines": [],
                        }

                        if context_lines > 0:
                            for ctx_line_num in range(context_start, context_end):
                                ctx_line_content = lines[ctx_line_num].rstrip("\n\r")
                                is_match_line = (ctx_line_num + 1) == line_num
                                match_info["context_lines"].append(
                                    {
                                        "line_num": ctx_line_num + 1,
                                        "content": ctx_line_content,
                                        "is_match": is_match_line,
                                    }
                                )

                        file_matches.append(match_info)
                        total_matches += 1

                        if total_matches >= max_results:
                            break

                # Add file results if there were matches
                if file_matches:
                    file_result_lines = [f"📄 {file_path}"]

                    for match in file_matches:
                        if context_lines > 0:
                            # Show context
                            for ctx in match["context_lines"]:
                                prefix = ">" if ctx["is_match"] else " "
                                file_result_lines.append(
                                    f"{prefix} {ctx['line_num']:4d}: {ctx['content']}"
                                )
                            file_result_lines.append("")  # Empty line between matches
                        else:
                            # Show just the matching line
                            file_result_lines.append(
                                f"  {match['line_num']:4d}: {match['line_content']}"
                            )

                    results.append("\n".join(file_result_lines))

            except Exception as e:
                # Skip files that can't be read
                continue

        if not results:
            pattern_desc = (
                f"regex pattern '{pattern}'" if regex else f"text '{pattern}'"
            )
            case_desc = " (case-sensitive)" if case_sensitive else " (case-insensitive)"
            return f"No matches found for {pattern_desc}{case_desc}"

        # Format final results
        match_count = len(results)
        header = f"Found matches in {match_count} files"
        if total_matches >= max_results:
            header += f" (limited to {max_results} total matches)"
        header += ":\n"

        return header + "\n" + "\n\n".join(results)

    except Exception as e:
        return f"Error in grep search: {str(e)}"


@tool(description=PATCH_DESCRIPTION)
def apply_patch(
    file_path: str,
    patch_content: str,
    create_backup: bool = True,
) -> str:
    """Apply a patch to a file.
    
    This function applies patches using git apply for reliable patch application.
    
    Args:
        file_path: Path to the file to patch
        patch_content: The patch content in unified diff format
        create_backup: Whether to create a backup of the original file before applying the patch
    
    Returns:
        Success or error message
    """
    try:
        path_obj = pathlib.Path(file_path)
        
        # Check if file exists
        if not path_obj.exists():
            return f"Error: File '{file_path}' not found"
        
        if not path_obj.is_file():
            return f"Error: '{file_path}' is not a file"
        
        # Create backup if requested
        backup_path = None
        if create_backup:
            backup_path = path_obj.with_suffix(path_obj.suffix + '.backup')
            shutil.copy2(path_obj, backup_path)
        
        # Use git apply for reliable patch application
        try:
            # Create a temporary patch file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.patch', delete=False) as temp_patch:
                temp_patch.write(patch_content)
                temp_patch_path = temp_patch.name
            
            # Apply the patch using git
            result = subprocess.run(
                ['git', 'apply', '--check', temp_patch_path],
                capture_output=True,
                text=True,
                cwd=path_obj.parent
            )
            
            if result.returncode != 0:
                # Patch check failed, clean up and return error
                os.unlink(temp_patch_path)
                if backup_path and backup_path.exists():
                    backup_path.unlink()
                return f"Error: Patch check failed: {result.stderr}"
            
            # Apply the patch
            result = subprocess.run(
                ['git', 'apply', temp_patch_path],
                capture_output=True,
                text=True,
                cwd=path_obj.parent
            )
            
            # Clean up temporary patch file
            os.unlink(temp_patch_path)
            
            if result.returncode != 0:
                # Patch application failed, restore backup
                if backup_path and backup_path.exists():
                    shutil.copy2(backup_path, path_obj)
                    backup_path.unlink()
                return f"Error applying patch: {result.stderr}"
            
            # Remove backup if patch was successful
            if backup_path and backup_path.exists():
                backup_path.unlink()
            
            return f"Successfully applied patch to '{file_path}' using git apply"
            
        except FileNotFoundError:
            # Git not available
            if backup_path and backup_path.exists():
                backup_path.unlink()
            return "Error: git not available on this system"
        except Exception as e:
            # Clean up on error
            if backup_path and backup_path.exists():
                shutil.copy2(backup_path, path_obj)
                backup_path.unlink()
            return f"Error using git apply: {str(e)}"
        
    except Exception as e:
        return f"Error applying patch: {str(e)}"
