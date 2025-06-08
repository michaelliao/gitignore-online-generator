#!/usr/bin/env python3

# generate git ignore list and copy files to _site.

import os, shutil


def copy_files(path, out_path, ext):
    fs = [f for f in os.listdir(path) if f.endswith(ext)]
    fs.sort()
    for f in fs:
        shutil.copy(os.path.join(path, f), os.path.join(out_path, f), follow_symlinks=True)
    return fs


def gen_js(ignores):
    s = ["'" + ig[:-10] + "'" for ig in ignores]
    return "[" + ", ".join(s) + "]"


def main():
    root_dir = os.getcwd()
    print(f"set root dir: {root_dir}")
    ignore_dir = os.path.join(root_dir, 'gitignore')
    script_dir = os.path.join(root_dir, "script")
    output_dir = os.path.join(root_dir, "_site")
    os.makedirs(os.path.join(output_dir, "Global"), exist_ok=True)

    print(f"copy language gitignore...")
    language_ignores = copy_files(ignore_dir, output_dir, ".gitignore")
    print(f"copy global gitignore...")
    global_ignores = copy_files(os.path.join(ignore_dir, "Global"), os.path.join(output_dir, "Global"), ".gitignore")

    print(f"copy staic files...")
    copy_files(script_dir, output_dir, ".ico")
    copy_files(script_dir, output_dir, ".html")
    copy_files(script_dir, output_dir, ".png")

    print(f"generate javascript...")
    js = f"""
// auto-generated ignore list:
window.language_ignores = {gen_js(language_ignores)};
window.global_ignores = {gen_js(global_ignores)};
"""
    with open(os.path.join(output_dir, "gitignore.js"), "w") as f:
        f.write(js)

    print("done.")

if __name__ == "__main__":
    main()
