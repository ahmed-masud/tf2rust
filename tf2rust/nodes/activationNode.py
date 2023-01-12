from .node import Node


class ActivationNode(Node):
    def __init__(self, layer_info, layer_weights):
        super().__init__(layer_info, layer_weights)
        self.activation_type = layer_info["config"]["activation"].capitalize()

    def can_be_done_inplace(self):
        return True

    def apply_layer(self):
        assert len(self.connections["inbounds"]) == 1
        assert len(self.input_shape) == len(self.output_shape)
        assert (
            len(self.parents_name) == 1
        ), "Node {} has parents {}. It should have exactly one parent".format(
            self.name, self.parents_name
        )

        if self.inplace_op:
            return [
                "tensorflow_layers::Activation::{node.activation_type}.activation_mut(&mut out_{input});".format(
                    node=self, input=self.parents_name[0]
                )
            ]
        else:
            return [
                "let {declare_mut}out_{node.name} = tensorflow_layers::Activation::{node.activation_type}.activation(&out_{input});".format(
                    declare_mut=self._format_mut(),
                    node=self,
                    input=self.parents_name[0],
                )
            ]
