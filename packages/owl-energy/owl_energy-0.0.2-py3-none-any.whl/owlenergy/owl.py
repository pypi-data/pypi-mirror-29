"""

"""
import logging
import re


logger = logging.getLogger(__name__)


class OWLDevice(object):
    def __init__(self, owl_id=None, last_update=None, signal_strength=None,
                 link_quality=None, battery_level=None, xml_string=None):
        """

        Args:
            owl_id (str):
            last_update (long):
            signal_strength (float):
            link_quality (float):
            battery_level (float):
            xml_string (str):
        """
        self.owl_id = owl_id
        self.last_update = last_update
        self.signal_strength = signal_strength
        self.battery_level = battery_level
        self.link_quality = link_quality

        if xml_string is not None:
            self.process_xml(xml_string)

    def process_xml(self, raw_data):
        """Read the device attributes from the OWL message buffer.

        """
        pattern = (r"<electricity id='(.*)'><timestamp>([0-9]*)<.*"
                   r".*rssi='(-[0-9]+)' lqi='([0-9]+)'.*"
                   r"level='([0-9]+)%.*")

        logger.info("Processing device data.")

        try:
            result = re.match(pattern, raw_data)

            if result is not None:
                self.owl_id = result.group(1)
                self.last_update = int(result.group(2))
                logger.debug("Timestamp: %f", self.last_update)
                self.signal_strength = float(result.group(3))
                logger.debug("Signal strength: %f", self.signal_strength)
                self.link_quality = float(result.group(4))
                logger.debug("Link quality: %f", self.link_quality)
                self.battery_level = float(result.group(5))
                logger.debug("Battery level: %f", self.battery_level)
            else:
                logger.warning("No device data available")
        except TypeError as error:
            logger.error(error)


class OWLEnergyReading(object):
    def __init__(self, channel=0, owl_id=None, current=None, total_current=None,
                 xml_string=None):
        """

        Args:
            channel (int):
            owl_id (str):
            current (float):
            total_current (float):
            xml_string (str):
        """
        self.current = current
        self.total_current = total_current
        self.channel = channel
        self.owl_id = owl_id

        if xml_string is not None:
            self.process_xml(xml_string)

    def process_xml(self, raw_data):
        """Extracts data from the OWL data buffer that matches the pattern.

        """
        pattern = (r"<electricity id='(.*)'><timestamp>.*chan id='({})'>"
                   r"<curr units='w'>([0-9]+\.[0-9]+)</curr>"
                   r"<day units='wh'>([0-9]+\.[0-9]+)"
                   r"</day.*").format(self.channel)

        try:
            result = re.match(pattern, raw_data)

            if result is not None:
                self.owl_id = result.group(1)
                self.channel = int(result.group(2))
                self.current = float(result.group(3))
                logger.debug("current: %f", self.current)
                self.total_current = float(result.group(4))
                logger.debug("total current: %f", self.total_current)
            else:
                logger.warning("No data available on channel %s", self.channel)

        except TypeError as error:
            logger.error(error)
