import pyvisa
from mock import patch, call
from src.equipments.bk8600 import Bk8600


class TestBk8600(object):
    @patch("{}.{}".format(Bk8600.__module__, pyvisa.__name__))
    def test_constructor(self, mock_pyvisa):
        # given
        resource_id = "USB0::65535"
        resource_manager = mock_pyvisa.ResourceManager.return_value
        instrument = resource_manager.open_resource.return_value

        # when
        Bk8600(resource_id)

        # then
        instrument.write.assert_called_with(Bk8600.RESET_COMMAND)
        instrument.query.assert_called_with(Bk8600.SELF_ID_QUERY)
        resource_manager.open_resource.assert_called_with(resource_id)

    @patch("{}.{}".format(Bk8600.__module__, pyvisa.__name__))
    def test_set_current(self, mock_pyvisa):
        # given
        py_instrument = mock_pyvisa.ResourceManager.return_value.open_resource.return_value
        current_a = 1
        instrument = Bk8600()
        py_instrument.reset_mock()

        # when
        instrument.set_current(current_a)

        # then
        py_instrument.write.assert_has_calls([
            call("{} {}".format(Bk8600.CURRENT_LEVEL_COMMAND, current_a)),
            call(Bk8600.INPUT_ON_CMD)
        ])
        py_instrument.query.assert_called_with("*OPC?")

    @patch("{}.{}".format(Bk8600.__module__, pyvisa.__name__))
    def test_toggle_eload_true(self, mock_pyvisa):
        # given
        state = True
        py_instrument = mock_pyvisa.ResourceManager.return_value.open_resource.return_value
        instrument = Bk8600()
        py_instrument.reset_mock()

        # when
        instrument.toggle_eload(state)

        # then
        py_instrument.write.assert_has_calls([
            call(Bk8600.INPUT_ON_CMD)
        ])

    @patch("{}.{}".format(Bk8600.__module__, pyvisa.__name__))
    def test_toggle_eload_false(self, mock_pyvisa):
        # given
        state = False
        py_instrument = mock_pyvisa.ResourceManager.return_value.open_resource.return_value
        instrument = Bk8600()
        py_instrument.reset_mock()

        # when
        instrument.toggle_eload(state)

        # then
        py_instrument.write.assert_has_calls([
            call(Bk8600.INPUT_OFF_CMD)
        ])

    @patch("{}.{}".format(Bk8600.__module__, pyvisa.__name__))
    def test_measure_voltage(self, mock_pyvisa):
        # given
        voltage = 30
        py_instrument = mock_pyvisa.ResourceManager.return_value.open_resource.return_value
        instrument = Bk8600()
        py_instrument.reset_mock()
        py_instrument.query.return_value = voltage

        # when
        v = instrument.measure_voltage()

        # then
        py_instrument.query.assert_called_with(Bk8600.DC_VOLTAGE_QUERY)
        assert v == voltage

    @patch("{}.{}".format(Bk8600.__module__, pyvisa.__name__))
    def test_measure_current(self, mock_pyvisa):
        # given
        current = 30
        py_instrument = mock_pyvisa.ResourceManager.return_value.open_resource.return_value
        instrument = Bk8600()
        py_instrument.reset_mock()
        py_instrument.query.return_value = current

        # when
        c = instrument.measure_current()

        # then
        py_instrument.query.assert_called_with(Bk8600.DC_CURRENT_QUERY)
        assert c == current
