"""
Test suite for CourierOptimizer core functionality.
"""

import pytest
import pandas as pd

from courier_optimizer.courier_optimizer import CourierOptimizer


class TestCourierOptimizer:
    """Test cases for the main CourierOptimizer class."""

    def test_courier_optimizer_initialization(self):
        """Test that CourierOptimizer can be initialized."""
        optimizer = CourierOptimizer()
        assert optimizer is not None
        assert hasattr(optimizer, 'validate_delivery')
        assert hasattr(optimizer, 'optimize_route')

    def test_valid_delivery_entry_passes_validation(self):
        """Test valid delivery entry validation."""
        optimizer = CourierOptimizer()
        
        valid_delivery = {
            'customer': 'Customer A',
            'latitude': 59.9139,
            'longitude': 10.7522,
            'priority': 'HIGH',
            'weight_kg': 15.5
        }
        
        result = optimizer.validate_delivery(valid_delivery)
        assert result['is_valid'] is True
        assert result['warnings'] == []

    def test_invalid_delivery_entry_fails_validation(self):
        """Test invalid delivery entry validation."""
        optimizer = CourierOptimizer()
        
        invalid_delivery = {
            'customer': 'Customer B',
            'latitude': 60.5,
            'longitude': 11.0,
            'priority': 'URGENT',
            'weight_kg': 30.0
        }
        
        result = optimizer.validate_delivery(invalid_delivery)
        assert result['is_valid'] is False
        assert len(result['warnings']) > 0
        assert any('weight' in warning.lower() for warning in result['warnings'])
        assert any('priority' in warning.lower() for warning in result['warnings'])
        assert any('coordinate' in warning.lower() or 'oslo' in warning.lower() 
                  for warning in result['warnings'])

    def test_csv_input_processing(self):
        """Test CSV file input processing."""
        optimizer = CourierOptimizer()
        
        sample_data = pd.DataFrame([
            {'customer': 'A', 'latitude': 59.9139, 'longitude': 10.7522, 
             'priority': 'HIGH', 'weight_kg': 15},
            {'customer': 'B', 'latitude': 59.9200, 'longitude': 10.7500, 
             'priority': 'LOW', 'weight_kg': 5},
            {'customer': 'C', 'latitude': 60.5, 'longitude': 11.0, 
             'priority': 'INVALID', 'weight_kg': 30}
        ])
        
        result = optimizer.process_csv_data(sample_data)
        
        assert 'valid_deliveries' in result
        assert 'invalid_deliveries' in result
        assert len(result['valid_deliveries']) == 2
        assert len(result['invalid_deliveries']) == 1
        assert result['invalid_deliveries'][0]['customer'] == 'C'

    def test_transport_mode_selection(self):
        """Test transport mode options."""
        optimizer = CourierOptimizer()
        
        valid_modes = ['CAR', 'BICYCLE', 'WALKING']
        for mode in valid_modes:
            assert optimizer.is_valid_transport_mode(mode) is True
        
        assert optimizer.is_valid_transport_mode('PLANE') is False
        assert optimizer.is_valid_transport_mode('TRAIN') is False

    def test_route_optimization_criteria(self):
        """Test route optimization criteria options."""
        optimizer = CourierOptimizer()
        
        valid_criteria = ['FASTEST', 'CHEAPEST', 'GREENEST']
        for criteria in valid_criteria:
            assert optimizer.is_valid_optimization_criteria(criteria) is True
        
        assert optimizer.is_valid_optimization_criteria('SHORTEST') is False