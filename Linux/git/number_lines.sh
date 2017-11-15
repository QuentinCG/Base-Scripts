# Show number of line of all Git repository in subfolders
# How to use: "source ./number_lines.sh"
for f in *; do
  if [[ -d $f ]]; then
    echo "------------$f------------"
    cd "$f"
    git ls-files | grep "\(.cpp\|.h\|.ino\|.php\|.html\|.htm\|.css\|.js\|.py\|.lua\|.bat\|.sh\)$" | xargs wc -l
    cd ..
  fi
done
