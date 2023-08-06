mdx_figcaption
==============

A quick-and-dirty markdown extension to create figure with captions

This markdown extension will take markdown like this

    ![placeholder](http://placehold.it/400x100/EFEFEF/76001D.png&text=Some+image "This text below the image is the caption. It is used to give some context to the image above.")
    
and transform it to HTML5-friendly

    <figure>
    <img src="http://placehold.it/400x100/EFEFEF/76001D.png&text=Some+image" alt="placeholder" title="This text below the image is the caption. It is used to give some context to the image above." />
    <figcaption>This text below the image is the caption. It is used to give some context to the image above.</figcaption>
    </figure>


It works by walking the markdown `etree` and wrapping every `img` tag with a `caption`  and `figcaption`.  The caption text is taken from the markdown (optional) title.
