<h1>itk-jupyter-widgets</h1>
<p><a href="https://github.com/InsightSoftwareConsortium/itk-jupyter-widgets/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License" /></a>
<a href="https://pypi.python.org/pypi/itkwidgets"><img src="https://img.shields.io/pypi/v/itkwidgets.svg" alt="PyPI" /></a>
<a href="https://circleci.com/gh/InsightSoftwareConsortium/itk-jupyter-widgets"><img src="https://circleci.com/gh/InsightSoftwareConsortium/itk-jupyter-widgets.svg?style=shield" alt="Build Status" /></a></p>
<p>Interactive <a href="https://jupyter.org/">Jupyter</a> widgets to visualize images in 2D and 3D.</p>
<img src="https://i.imgur.com/ERK5JtT.png" width="800" alt="Monkey brain volume rendering">
<p>These widgets are designed to support image analysis with the <a href="https://itk.org/">Insight Toolkit
(ITK)</a>, but they also work with other spatial analysis tools
in the scientific Python ecosystem.</p>
<p>These widgets are built on
<a href="https://github.com/InsightSoftwareConsortium/itk-js">itk.js</a> and
<a href="https://github.com/Kitware/vtk-js">vtk.js</a>.</p>
<h2>Installation</h2>
<p>To install, use pip:</p>
<pre><code class="language-sh">pip install itkwidgets
jupyter nbextension enable --py --sys-prefix itkwidgets
</code></pre>
<p>For a development installation (requires <a href="https://nodejs.org/en/download/">Node.js</a>),</p>
<pre><code class="language-sh">git clone https://github.com/InsightSoftwareConsortium/itk-jupyter-widgets.git
cd itk-jupyter-widgets
python -m pip install -r requirements-dev.txt -r requirements.txt
python -m pip install -e .
jupyter nbextension install --py --symlink --sys-prefix itkwidgets
jupyter nbextension enable --py --sys-prefix itkwidgets
jupyter nbextension enable --py --sys-prefix widgetsnbextension
python -m pytest
</code></pre>


