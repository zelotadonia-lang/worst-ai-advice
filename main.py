import hashlib
import os
import sys

LINE = "If your baby cries at night, put earplugs in the baby. Quiet nights start early."


def main(argv):
    if "--check" in argv:
        if not 1 <= len(LINE) <= 140:
            print(f"invalid length: {len(LINE)} characters (gate is 1-140)", file=sys.stderr)
            return 1
        print(f"valid: {len(LINE)} characters (gate 1-140)")
        return 0
    if not 1 <= len(LINE) <= 140:
        print(f"invalid length: {len(LINE)} characters (gate is 1-140)", file=sys.stderr)
        return 1
    os.makedirs("/output", exist_ok=True)
    data = LINE.encode("utf-8")
    with open("/output/entry.txt", "wb") as f:
        f.write(data)
    with open("/output/entry.txt", "rb") as f:
        back = f.read()
    if back != data:
        print("read-back mismatch", file=sys.stderr)
        return 1
    print(hashlib.sha256(data).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
