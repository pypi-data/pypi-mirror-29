class VehicleDevice:
    def __init__(self, data, controller):
        self._id = data['id']
        self._vin = data['vin']
        self._raw_name = data['name']
        self._short_name = ' '.join(self._raw_name.split()[:3])
        self._controller = controller
        self.should_poll = True

        self.imghost = 'https://connectedcars.imgix.net'
        self._img_path = data['imageFilename']

    def _name(self):
        return "{} {}".format(self._short_name, self.type)

    def _uniq_name(self):
        return '{} {} {}'.format(self._short_name, self._id, self.type)

    def _img_url(self):
        return '{}{}'.format(self.imghost, self._img_path)
