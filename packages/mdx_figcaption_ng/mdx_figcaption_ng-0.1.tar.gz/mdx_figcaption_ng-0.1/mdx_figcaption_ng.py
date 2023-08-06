import markdown
from markdown.util import etree


class MarkdownCaption(markdown.treeprocessors.Treeprocessor):
    def run(self,root):
        self.search_and_change(root)
        return root

    def iterparent(self, tree):
        for parent in tree.getiterator():
            for child in parent:
                yield parent, child

    # Added check to see if img is already wrapped up in figure.
    def search_and_change(self, element):
        for parent, child in list(self.iterparent(element)):
            if child.tag == "img" and parent.tag != "figure":
                d = child.attrib.copy()

                child.clear()
                child.tag = "figure"

                img = etree.Element("img")
                img.attrib = d

                child.append(img)

                caption = etree.Element("figcaption")
                caption.text = d.get("title", "")

                child.append(caption)


# The rest is unchanged.
class CaptionsExtension(markdown.extensions.Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors["figures"] = MarkdownCaption(md)
        md.registerExtension(self)


def makeExtension(configs=None):
    return CaptionsExtension(configs)
