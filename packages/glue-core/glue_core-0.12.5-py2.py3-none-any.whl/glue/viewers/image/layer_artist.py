from __future__ import absolute_import, division, print_function

import uuid
import weakref

import numpy as np

from glue.utils import defer_draw

from glue.viewers.image.state import ImageLayerState, ImageSubsetLayerState
from glue.viewers.matplotlib.layer_artist import MatplotlibLayerArtist
from glue.core.exceptions import IncompatibleAttribute
from glue.utils import color2rgb
from glue.core.link_manager import is_equivalent_cid
from glue.core import Data, HubListener
from glue.core.message import ComponentsChangedMessage
from glue.external.modest_image import imshow


class BaseImageLayerArtist(MatplotlibLayerArtist, HubListener):

    def __init__(self, axes, viewer_state, layer_state=None, layer=None):

        super(BaseImageLayerArtist, self).__init__(axes, viewer_state,
                                                   layer_state=layer_state, layer=layer)

        self.reset_cache()

        # Watch for changes in the viewer state which would require the
        # layers to be redrawn
        self._viewer_state.add_global_callback(self._update_image)
        self.state.add_global_callback(self._update_image)

        self.layer.hub.subscribe(self, ComponentsChangedMessage,
                                 handler=self._update_compatibility,
                                 filter=self._is_data_object)

        self._update_compatibility()

    def _is_data_object(self, message):
        if isinstance(self.layer, Data):
            return message.sender is self.layer
        else:
            return message.sender is self.layer.data

    def reset_cache(self):
        self._last_viewer_state = {}
        self._last_layer_state = {}

    def _update_image(self, force=False, **kwargs):
        raise NotImplementedError()

    @defer_draw
    def _update_compatibility(self, *args, **kwargs):
        """
        Determine compatibility of data with reference data. For the data to be
        compatible with the reference data, the number of dimensions has to
        match and the pixel component IDs have to be equivalent.
        """

        if self._viewer_state.reference_data is None:
            self._compatible_with_reference_data = False
            self.disable('No reference data defined')
            return

        if self.layer is self._viewer_state.reference_data:
            self._compatible_with_reference_data = True
            self.enable()
            return

        # Check whether the pixel component IDs of the dataset are equivalent
        # to that of the reference dataset. In future this is where we could
        # allow for these to be different and implement reprojection.
        if self.layer.ndim != self._viewer_state.reference_data.ndim:
            self._compatible_with_reference_data = False
            self.disable('Data dimensions do not match reference data')
            return

        # Determine whether pixel component IDs are equivalent

        pids = self.layer.pixel_component_ids
        pids_ref = self._viewer_state.reference_data.pixel_component_ids

        if isinstance(self.layer, Data):
            data = self.layer
        else:
            data = self.layer.data

        for i in range(data.ndim):
            if not is_equivalent_cid(data, pids[i], pids_ref[i]):
                self._compatible_with_reference_data = False
                self.disable('Pixel component IDs do not match. You can try '
                             'fixing this by linking the pixel component IDs '
                             'of this dataset with those of the reference '
                             'dataset.')
                return

        self._compatible_with_reference_data = True
        self.enable()


class ImageLayerArtist(BaseImageLayerArtist):

    _layer_state_cls = ImageLayerState

    def __init__(self, axes, viewer_state, layer_state=None, layer=None):

        super(ImageLayerArtist, self).__init__(axes, viewer_state,
                                               layer_state=layer_state, layer=layer)

        # We use a custom object to deal with the compositing of images, and we
        # store it as a private attribute of the axes to make sure it is
        # accessible for all layer artists.
        self.uuid = str(uuid.uuid4())
        self.composite = self.axes._composite
        self.composite.allocate(self.uuid)
        self.composite.set(self.uuid, array=self.get_image_data,
                           shape=self.get_image_shape)
        self.composite_image = self.axes._composite_image

    def get_layer_color(self):
        if self._viewer_state.color_mode == 'One color per layer':
            return self.state.color
        else:
            return self.state.cmap

    def enable(self):
        if hasattr(self, 'composite_image'):
            self.composite_image.invalidate_cache()
        super(ImageLayerArtist, self).enable()

    def remove(self):
        super(ImageLayerArtist, self).remove()
        if self.uuid in self.composite:
            self.composite.deallocate(self.uuid)

    def get_image_shape(self):

        if not self._compatible_with_reference_data:
            return None

        if self._viewer_state.x_att is None or self._viewer_state.y_att is None:
            return None

        x_axis = self._viewer_state.x_att.axis
        y_axis = self._viewer_state.y_att.axis

        full_shape = self.layer.shape

        return full_shape[y_axis], full_shape[x_axis]

    def get_image_data(self, view=None):

        if not self._compatible_with_reference_data:
            return None

        try:
            image = self.state.get_sliced_data(view=view)
        except (IncompatibleAttribute, IndexError):
            # The following includes a call to self.clear()
            self.disable_invalid_attributes(self.state.attribute)
            return None
        else:
            self.enable()

        return image

    def _update_image_data(self):
        self.composite_image.invalidate_cache()
        self.redraw()

    @defer_draw
    def _update_visual_attributes(self):

        if not self.enabled:
            return

        if self._viewer_state.color_mode == 'Colormaps':
            color = self.state.cmap
        else:
            color = self.state.color

        self.composite.set(self.uuid,
                           clim=(self.state.v_min, self.state.v_max),
                           visible=self.state.visible,
                           zorder=self.state.zorder,
                           color=color,
                           contrast=self.state.contrast,
                           bias=self.state.bias,
                           alpha=self.state.alpha,
                           stretch=self.state.stretch)

        self.composite_image.invalidate_cache()

        self.redraw()

    @defer_draw
    def _update_image(self, force=False, **kwargs):

        if self.state.attribute is None or self.state.layer is None:
            return

        # Figure out which attributes are different from before. Ideally we shouldn't
        # need this but currently this method is called multiple times if an
        # attribute is changed due to x_att changing then hist_x_min, hist_x_max, etc.
        # If we can solve this so that _update_histogram is really only called once
        # then we could consider simplifying this. Until then, we manually keep track
        # of which properties have changed.

        changed = set()

        if not force:

            for key, value in self._viewer_state.as_dict().items():
                if value != self._last_viewer_state.get(key, None):
                    changed.add(key)

            for key, value in self.state.as_dict().items():
                if value != self._last_layer_state.get(key, None):
                    changed.add(key)

        self._last_viewer_state.update(self._viewer_state.as_dict())
        self._last_layer_state.update(self.state.as_dict())

        if 'reference_data' in changed or 'layer' in changed:
            self._update_compatibility()

        if force or any(prop in changed for prop in ('layer', 'attribute',
                                                     'slices', 'x_att', 'y_att')):
            self._update_image_data()
            force = True  # make sure scaling and visual attributes are updated

        if force or any(prop in changed for prop in ('v_min', 'v_max', 'contrast',
                                                     'bias', 'alpha', 'color_mode',
                                                     'cmap', 'color', 'zorder',
                                                     'visible', 'stretch')):
            self._update_visual_attributes()

    @defer_draw
    def update(self):

        self._update_image(force=True)

        # Reset the axes stack so that pressing the home button doesn't go back
        # to a previous irrelevant view.
        self.axes.figure.canvas.toolbar.update()

        self.redraw()


class ImageSubsetArray(object):

    def __init__(self, viewer_state, layer_artist):
        self._viewer_state = weakref.ref(viewer_state)
        self._layer_artist = weakref.ref(layer_artist)
        self._layer_state = weakref.ref(layer_artist.state)

    @property
    def layer_artist(self):
        return self._layer_artist()

    @property
    def layer_state(self):
        return self._layer_state()

    @property
    def viewer_state(self):
        return self._viewer_state()

    @property
    def shape(self):

        if not self.layer_artist._compatible_with_reference_data:
            return None

        x_axis = self.viewer_state.x_att.axis
        y_axis = self.viewer_state.y_att.axis

        full_shape = self.layer_state.layer.shape

        return full_shape[y_axis], full_shape[x_axis]

    def __getitem__(self, view=None):

        if (self.layer_artist is None or
                self.layer_state is None or
                self.viewer_state is None):
            return None

        if not self.layer_artist._compatible_with_reference_data:
            return None

        try:
            mask = self.layer_state.get_sliced_data(view=view)
        except IncompatibleAttribute:
            self.layer_artist.disable_incompatible_subset()
            return None
        else:
            self.layer_artist.enable()

        r, g, b = color2rgb(self.layer_state.color)
        mask = np.dstack((r * mask, g * mask, b * mask, mask * .5))
        mask = (255 * mask).astype(np.uint8)

        return mask

    @property
    def dtype(self):
        return np.uint8

    @property
    def ndim(self):
        return 2

    @property
    def size(self):
        return np.product(self.shape)


class ImageSubsetLayerArtist(BaseImageLayerArtist):

    _layer_state_cls = ImageSubsetLayerState

    def __init__(self, axes, viewer_state, layer_state=None, layer=None):

        super(ImageSubsetLayerArtist, self).__init__(axes, viewer_state,
                                                     layer_state=layer_state, layer=layer)

        self.subset_array = ImageSubsetArray(self._viewer_state, self)

        self.image_artist = imshow(self.axes, self.subset_array,
                                   origin='lower', interpolation='nearest',
                                   vmin=0, vmax=1, aspect=self._viewer_state.aspect)
        self.mpl_artists = [self.image_artist]

    @defer_draw
    def _update_visual_attributes(self):

        if not self.enabled:
            return

        # TODO: deal with color using a colormap instead of having to change data

        self.image_artist.set_visible(self.state.visible)
        self.image_artist.set_zorder(self.state.zorder)
        self.image_artist.set_alpha(self.state.alpha)

        self.redraw()

    def _update_image(self, force=False, **kwargs):

        if self.state.layer is None:
            return

        # Figure out which attributes are different from before. Ideally we shouldn't
        # need this but currently this method is called multiple times if an
        # attribute is changed due to x_att changing then hist_x_min, hist_x_max, etc.
        # If we can solve this so that _update_histogram is really only called once
        # then we could consider simplifying this. Until then, we manually keep track
        # of which properties have changed.

        changed = set()

        if not force:

            for key, value in self._viewer_state.as_dict().items():
                if value != self._last_viewer_state.get(key, None):
                    changed.add(key)

            for key, value in self.state.as_dict().items():
                if value != self._last_layer_state.get(key, None):
                    changed.add(key)

        self._last_viewer_state.update(self._viewer_state.as_dict())
        self._last_layer_state.update(self.state.as_dict())

        if 'reference_data' in changed or 'layer' in changed:
            self._update_compatibility()

        if force or any(prop in changed for prop in ('layer', 'attribute', 'color',
                                                     'x_att', 'y_att', 'slices')):
            self.image_artist.invalidate_cache()
            self.redraw()  # forces subset to be recomputed
            force = True  # make sure scaling and visual attributes are updated

        if force or any(prop in changed for prop in ('zorder', 'visible', 'alpha')):
            self._update_visual_attributes()

    def enable(self):
        super(ImageSubsetLayerArtist, self).enable()
        # We need to now ensure that image_artist, which may have been marked
        # as not being visible when the layer was cleared is made visible
        # again.
        if hasattr(self, 'image_artist'):
            self.image_artist.invalidate_cache()
            self._update_visual_attributes()

    @defer_draw
    def update(self):
        # TODO: determine why this gets called when changing the transparency slider
        self._update_image(force=True)
        self.redraw()
