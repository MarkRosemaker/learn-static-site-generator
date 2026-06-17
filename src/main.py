from funcs import generate_pages_recursive
import os, shutil

DIR_STATIC = "static"
DIR_DST = "public"


def copy_to_destination():
    if os.path.exists(DIR_DST):
        shutil.rmtree(DIR_DST)

    copy_to_destination_recursive(DIR_STATIC, DIR_DST)


def copy_to_destination_recursive(src: str, dst: str):
    if os.path.isfile(src):
        print(f"Copying {dst}...")
        shutil.copy(src, dst)
        return

    print(f"Creating {dst}/...")
    os.mkdir(dst)

    for f in os.listdir(src):
        copy_to_destination_recursive(os.path.join(src, f), os.path.join(dst, f))


def main():
    copy_to_destination()
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
