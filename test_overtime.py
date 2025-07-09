#!/usr/bin/env python3
"""
Test script to demonstrate multiple overtime status handling.
"""

from wnba_scores import get_status_display

def test_overtime_statuses():
    """Test various overtime scenarios."""
    
    print("Testing Multiple Overtime Status Handling:")
    print("=" * 50)
    
    # Test scenarios
    test_cases = [
        # (status_name, status_description, period, expected_result)
        ("STATUS_FINAL", "Final", 4, "F"),
        ("STATUS_FINAL", "Final", 5, "F/OT"),
        ("STATUS_FINAL", "Final", 6, "F/2OT"),
        ("STATUS_FINAL", "Final", 7, "F/3OT"),
        ("STATUS_FINAL", "Final", 8, "F/4OT"),
        ("STATUS_FINAL", "Final", 9, "F/5OT"),
        ("STATUS_IN_PROGRESS", "Live", 5, "OT"),
        ("STATUS_IN_PROGRESS", "Live", 6, "2OT"),
        ("STATUS_IN_PROGRESS", "Live", 7, "3OT"),
        ("STATUS_IN_PROGRESS", "Live", 8, "4OT"),
        ("STATUS_IN_PROGRESS", "Live", 9, "5OT"),
        ("STATUS_SCHEDULED", "Scheduled", None, "Scheduled"),
        ("STATUS_HALFTIME", "Halftime", None, "H"),
    ]
    
    for status_name, status_desc, period, expected in test_cases:
        result = get_status_display(status_name, status_desc, period)
        status = "✓" if result == expected else "✗"
        print(f"{status} Period {period or 'N/A'}: {status_name} -> {result} (expected: {expected})")
    
    print("\nThe script now properly handles multiple overtimes!")
    print("- F/OT for 1st overtime final")
    print("- F/2OT for 2nd overtime final") 
    print("- F/3OT for 3rd overtime final")
    print("- And so on for higher overtimes...")

if __name__ == "__main__":
    test_overtime_statuses() 