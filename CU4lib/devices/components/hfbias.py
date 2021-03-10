from .descriptors import (
        CU4ComponentContainer,
        CU4FloatValue,
        CU4BoolValue,
        CU4ReadOnly
    )


class CU4CurrentHFBias(CU4ComponentContainer):
    """ CU4CurrentHFBias 
        
        Properties
        ----------
        current : float | None
            the bias current
        voltage : float | None
            the bias voltage
        hf_enabled : bool | None
            Returns high frequency mode state
        
        API
        ---
        enable_hf() : None
            Enables high frequency mode.
        disable_hf() : None
            Disables high frequency mode.

    """
    voltage = CU4ReadOnly(CU4FloatValue("VOLT"))
    hf_enabled = CU4ReadOnly(CU4BoolValue("HFME"))
    _current = CU4FloatValue("CURR")
    _current_m = CU4ReadOnly(CU4FloatValue("CURM"))
    _hf_enabled_cache = None

    @property
    def current(self):
        if self._hf_enabled_cache is None:
            self._hf_enabled_cache = hf_enabled
            if self.action_failed:
                return None
        if self._hf_enabled_cache:
            return self._current_m
        else:
            return self._current
    
    @current.setter
    def current(self, x):
        self._current = x

    def enable_hf(self):
        self._set_override_ro("hf_enabled", True)
        if not self.action_failed:
            self._hf_enabled_cache = True
    
    def disable_hf(self):
        self._set_override_ro("hf_enabled", False)
        if not self.action_failed:
            self._hf_enabled_cache = False
