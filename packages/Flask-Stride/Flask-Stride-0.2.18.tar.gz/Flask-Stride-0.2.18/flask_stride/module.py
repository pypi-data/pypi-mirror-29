class Module(object):
    """Base class for Stride app modules."""

    type = None

    def __init__(self, key):
        self.properties = {}
        self.properties['key'] = key

    def add_property(self, property, value):
        if getattr(self, 'properties', None) is None:
            self.properties = {}
        self.properties[property] = value

    def get_property(self, property):
        if getattr(self, 'properties', None) is None:
            return None
        if property in self.properties:
            return self.properties[property]
        else:
            return None

    def del_property(self, property):
        if property in self.properties:
            del(self.properties[property])

    def to_descriptor(self):
        """Output app descriptor data as a dict."""
        return self._descriptor_value(self.properties)

    def _descriptor_value(self, value):
        output_value = value
        # If the value is a Module (or subclass) object...
        if issubclass(type(value), Module):
            output_value = value.to_descriptor()
        # If dict, recurse over the elements of the list...
        elif isinstance(value, list):
            output_value = []
            for elem in value:
                output_value.append(self._descriptor_value(elem))
        # If dict, recurse over the dict...
        elif isinstance(value, dict):
            output_value = {}
            for k in value:
                output_value[k] = self._descriptor_value(value[k])
        return output_value
