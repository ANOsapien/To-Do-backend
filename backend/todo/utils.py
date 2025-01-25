from datetime import time
from .constants import TIME_SLOT_MAPPINGS

def get_slot_timing(slot_code):
    """
    Get the timing details for a given slot code
    """
    return TIME_SLOT_MAPPINGS.get(slot_code)

def is_slot_available(slot_code, check_time):
    """
    Check if a given time falls within a slot's timing
    """
    slot_info = TIME_SLOT_MAPPINGS.get(slot_code)
    if not slot_info:
        return False
    
    return slot_info['start'] <= check_time <= slot_info['end']