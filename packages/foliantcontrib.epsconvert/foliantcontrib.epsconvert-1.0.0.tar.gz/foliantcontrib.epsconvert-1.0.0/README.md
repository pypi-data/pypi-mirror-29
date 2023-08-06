# EPSConvert

EPSConvert is a tool to convert EPS images into PNG format. This operation applies to any target excluding `pdf`.

## Installation

```bash
$ pip install foliantcontrib.epsconvert
```

## Config

To enable the preprocessor, add `epsconvert` to `preprocessors` section in the project config:

```yaml
preprocessors:
    - epsconvert
```

The preprocessor has a number of options:

```yaml
preprocessors:
    - epsconvert:
        mogrify_path: mogrify
        image_width: 1500
```

`mogrify_path`
:   Path to the `morgify` binary. By default, it is assumed that you have this command in `PATH`. [ImageMagick](https://imagemagick.org/) must be installed.

`image_width`
:   Width of PNG images in pixels. By default, the width of each image is set by ImageMagick automatically. Default behavior is recommended. If the width is given explicitly, file size may increase.
