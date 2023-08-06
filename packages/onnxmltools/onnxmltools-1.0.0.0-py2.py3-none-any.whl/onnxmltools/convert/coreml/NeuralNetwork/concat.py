#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

from ...common import NodeBuilder
from ...common import utils
from ...common import registration
from .reshape import extend_inputs_from_2d_to_4d

class ConcatLayerConverter:

    @staticmethod
    def validate(cm_node):
        try:
            utils._check_has_attr(cm_node, 'name')
            utils._check_has_attr(cm_node, 'input')
            utils._check_has_attr(cm_node, 'output')
        except AttributeError as e:
            raise RuntimeError('Missing attribute in neural network layer: {0}'.format(cm_node.name))

    @staticmethod
    def convert(context, cm_node, inputs, outputs):
        extend_inputs_from_2d_to_4d(context, inputs)

        nb = NodeBuilder(context, 'Concat')
        if cm_node.concat.sequenceConcat:
            nb.add_attribute('axis', 0)
        else:
            nb.add_attribute('axis', 1)
        nb.extend_inputs(inputs)
        nb.extend_outputs(outputs)

        return nb.make_node()

registration.register_nn_converter('concat', ConcatLayerConverter)
