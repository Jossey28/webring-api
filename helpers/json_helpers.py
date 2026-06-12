from pathlib import Path
import io
import tempfile
from typing import TypeAlias
from pydantic import BaseModel, TypeAdapter, Field, ValidationError
from fastapi_globals import g
from fastapi_utils.tasks import repeat_every


class Member(BaseModel):
    index: int = Field(gt=0)
    owner: str
    site: str

    ring_name: str


MemberList: TypeAlias = list[Member]
MemberListModel = TypeAdapter(MemberList)

input_buffer = (
    io.BytesIO()
)  # TODO! Figure out non-global method of implenting shared state across files. fastapi_globals isn't working for the buffer


def load_data():
    path: Path = g.json_path
    raw_json = path.read_text()
    members: list[Member] = list()
    ignore_order = False

    for index, line in enumerate(raw_json.splitlines()):
        try:
            member_line = Member.model_validate_json(line)
            if (index + 1) != member_line.index and not ignore_order:
                print(
                    f"\nLine {index} contains index {member_line.index}, this means your jsonl file- indexs aren't sequential, is this intended?"
                )

                should_ignore_order = input("y/N: ")
                if should_ignore_order.lower() == "y":
                    ignore_order = True
                    print(
                        "\nSince this is intended the program won't stop for this again"
                    )
                else:
                    print("\nSince this isn't intended, do you want to exit safetly?")
                    exit_safely = input("Y/n: ")
                    if exit_safely.lower() == "n":
                        continue
                    else:
                        import sys

                        sys.exit(1)

            members.append(member_line)
        except ValidationError as e:
            print(
                f"Failed to validate line {index}: {line}\nError: {e}\n\nShould this line be skipped?"
            )
            answer = input("y/N: ")
            if answer.lower() == "y":
                continue
            else:
                import sys

                sys.exit(1)

    input_buffer.write(MemberListModel.dump_json(members))
    input_buffer.seek(0)  # Go back to start since write leaves it at the end


def read_input_buffer() -> bytes:
    try:
        return input_buffer.read()
    except Exception as e:
        import sys

        print(f"Unable to read input buffer: {e}\nQuitting Early")
        sys.exit(1)


def write_input_buffer(member: str):
    try:
        member_valid = Member.model_validate_json(member)
        input_buffer.write(Member.model_dump_json(member_valid).encode("utf-8"))
    except ValidationError as e:
        print(f"Coudln't validate {member}\nError: {e}")
        raise
    except Exception as e:
        print(
            f"Caught unknown exception in write_input_buffer function\nError: {e}\nContinuing execution"
        )


@repeat_every(seconds=60 * 5)  # Every 5 minutes we save to disk
async def save_data() -> None:
    import os

    path: Path = g.json_path
    input_buffer: io.BytesIO = g.input_buffer

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jsonl") as tmp_file:
        tmp_file.write(
            input_buffer.read()
        )  # Write to tmp to prevent data corruption. os.replace is instant (atmoic); https://stackoverflow.com/questions/51862186/is-os-replace-atomic-on-windows

    os.replace(tmp_file.name, path)
