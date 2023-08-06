Introduction 
============

WinMLTools enables you to convert models from different machine 
learning toolkits into `ONNX <https://onnx.ai>`_ for use with Windows Machine Learning. 
Currently the following toolkits are supported:

* Apple CoreML
* scikit-learn
  (subset of models convertible to ONNX)
* LibSVM
* XGBoost

Install
=======

::

    pip install winmltools

Dependancies
============

This converter package extends the functionalities of 
`ONNXMLTools <http://github.com/onnx/onnxmltools/>`_.

`scikit-learn <http://scikit-learn.org/stable/>`_ is needed to convert
a scikit-learn model, `coremltools <https://pypi.python.org/pypi/coremltools>`_
for Apple CoreML.


Example
=======

Here is a simple example to convert a CoreML model:

::

    import winmltools
    import coremltools

    model_coreml = coremltools.utils.load_spec("image_recognition.mlmodel")
    model_onnx = winmltools.convert.convert_coreml(model_coreml, "Image_Reco")

    # Save as text
    winmltools.utils.save_text(model_onnx, "image_recognition.json")

    # Save as protobuf
    winmltools.utils.save_model(model_onnx, "image_recognition.onnx")

License
=======

MIT License


