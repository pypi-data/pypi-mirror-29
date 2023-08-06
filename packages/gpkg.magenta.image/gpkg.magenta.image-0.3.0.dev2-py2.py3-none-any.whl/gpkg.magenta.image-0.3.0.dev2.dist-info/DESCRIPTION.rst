
Models
######

magenta-arbitrary-stylize
#########################

*Fast artistic style transfer using arbitrary painting styles*

Operations
==========

generate
^^^^^^^^

*Generate a stylized using model pretrained on PNB and DRD images*

Flags
-----

**content-images**
  *Path to content images (include glob pattern matching images) (required)*

**image-size**
  *Size of images (default is 1024)*

**interpolation-weights**
  *Interpolation weights This value is a list of float values inside square
  brackets. Each value is a weight for interpolation between the parameters
  of the identity transform and the style parameters of the style image. The
  larger the weight is the strength of stylization is more. Weight of 1.0
  means the normal style transfer and weight of 0.0 means identity
  transform. (default is '[1.0]')*

**style-images**
  *Path to style images (include glob pattern matching images) (required)*

References
==========

- https://github.com/tensorflow/magenta/tree/master/magenta/models/arbitrary_image_stylization
- https://arxiv.org/abs/1705.06830
- https://arxiv.org/abs/1610.07629
- https://arxiv.org/abs/1603.08155
- https://arxiv.org/abs/1508.06576

magenta-image-stylize
#####################

*Implementation of 'A Learned Representation for Artistic Style'*

Operations
==========

generate
^^^^^^^^

*Generate a stylized image using a pretrained models*

Flags
-----

**image**
  *Image to stylize (required)*

**style**
  *Style to apply (monet or varied) (required)*

References
==========

- https://github.com/tensorflow/magenta/tree/master/magenta/models/image_stylization
- https://arxiv.org/abs/1610.07629


