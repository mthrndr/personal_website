import os
import re
import markdown

# Finds the component tags, denoted by <-- and -->
# Note that the component name can only be a-z A-Z 0-9 and _-
COMP_RE = re.compile(r"<--\s*([a-zA-Z0-9_-]+?)(?:\s+(.*?))?\s*-->", re.DOTALL)
# Finds the markdown tags, denoted by <#-- and -->
# If you want to use the markdown file test.md then the tag is
# <#-- test -->
MARKDOWN_RE = re.compile(r"<#--\s*(.*?)\s*-->", re.DOTALL)
# Component attributes, ie <--component_name color="red" type="cool"-->
# In the actual file where the attribute is used it is denoted as /*attribute*/
ATTRIBUTE_RE = re.compile(r'([a-zA-Z0-9_-]+)="([^"]*)"')


def compile_page(html):
    while True:
        comp_match = COMP_RE.search(html)
        md_match = MARKDOWN_RE.search(html)

        if not (comp_match or md_match):
            break

        if comp_match:
            full_comp_tag = comp_match.group(0)
            comp_nm = comp_match.group(1)
            comp_attr_str = comp_match.group(2)
            comp_file = f"src/components/{comp_nm}.html"

            if os.path.exists(comp_file):

                with open(comp_file, "r", encoding="utf-8") as f:
                    comp_html = f.read()

                if comp_attr_str:
                    attrs = ATTRIBUTE_RE.findall(comp_attr_str)
                    for attr_nm, attr_val in attrs:
                        comp_html = comp_html.replace(
                                        f"/*{attr_nm}*/",
                                        attr_val
                                    )

                html = html.replace(full_comp_tag, comp_html)
            else:
                raise FileNotFoundError(f"Could not find component: {comp_file}")

        if md_match:
            full_md_tag = md_match.group(0)
            md_nm = md_match.group(1)
            md_file = f"src/markdown/{md_nm}.md"

            if os.path.exists(md_file):
                with open(md_file, "r", encoding="utf-8") as f:
                    md_content = markdown.markdown(f.read())

                html = html.replace(full_md_tag, md_content)

            else:
                raise FileNotFoundError(f"Could not find markdown: {md_file}")

    return html


def main() -> None:
    # Create generated directory
    os.makedirs("gen", exist_ok=True)
    for file in os.listdir('src'):
        if file.endswith(".css"):
            with open(f"src/{file}", "r") as src, open(f"gen/{file}", "w") as dest:
                dest.write(src.read())

    for file in os.listdir("src"):
        if file.endswith(".html"):
            compiled = None
            with open(f"src/{file}", "r", encoding="utf-8") as f:
                compiled = compile_page(f.read())
            with open(f"gen/{file}", "w", encoding="utf-8") as f:
                f.write(compiled)


if __name__ == "__main__":
    main()
