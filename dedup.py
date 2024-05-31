from os import listdir

files = {}
lines_ = {}

for file in listdir("output"):
    name = file.split("_")[0]
    path = "output/" + file
    files[name] = files.get(name, []) + [path]

for name, paths in files.items():
    lines_uniq = set()
    for path in paths:
        with open(path, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()[1:]
            for line in lines:
                lines_uniq.add(line)
    lines_[name] = lines_uniq

for name, uniqlines in lines_.items():
    with open(name + ".csv", "w", encoding="utf-8-sig") as f:
        f.write("名称,电话,网址\n")
        f.write("".join(sorted(uniqlines)))
