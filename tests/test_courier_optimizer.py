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
        assert hasattr(optimizer, "validate_delivery")
        assert hasattr(optimizer, "optimize_route")

    def test_valid_delivery_entry_passes_validation(self):
        """Test valid delivery entry validation."""
        optimizer = CourierOptimizer()

        valid_delivery = {
            "customer": "Customer A",
            "latitude": 59.9139,
            "longitude": 10.7522,
            "priority": "HIGH",
            "weight_kg": 15.5,
        }

        result = optimizer.validate_delivery(valid_delivery)
        assert result["is_valid"] is True
        assert result["warnings"] == []

    def test_invalid_delivery_entry_fails_validation(self):
        """Test invalid delivery entry validation."""
        optimizer = CourierOptimizer()

        invalid_delivery = {
            "customer": "Customer B",
            "latitude": 60.5,
            "longitude": 11.0,
            "priority": "URGENT",
            "weight_kg": 30.0,
        }

        result = optimizer.validate_delivery(invalid_delivery)
        assert result["is_valid"] is False
        assert len(result["warnings"]) > 0
        assert any("weight" in warning.lower() for warning in result["warnings"])
        assert any("priority" in warning.lower() for warning in result["warnings"])
        assert any(
            "coordinate" in warning.lower() or "oslo" in warning.lower()
            for warning in result["warnings"]
        )

    def test_csv_input_processing(self):
        """Test CSV file input processing."""
        optimizer = CourierOptimizer()

        sample_data = pd.DataFrame(
            [
                {
                    "customer": "A",
                    "latitude": 59.9139,
                    "longitude": 10.7522,
                    "priority": "HIGH",
                    "weight_kg": 15,
                },
                {
                    "customer": "B",
                    "latitude": 59.9200,
                    "longitude": 10.7500,
                    "priority": "LOW",
                    "weight_kg": 5,
                },
                {
                    "customer": "C",
                    "latitude": 60.5,
                    "longitude": 11.0,
                    "priority": "INVALID",
                    "weight_kg": 30,
                },
            ]
        )

        result = optimizer.process_csv_data(sample_data)

        assert "valid_deliveries" in result
        assert "invalid_deliveries" in result
        assert len(result["valid_deliveries"]) == 2
        assert len(result["invalid_deliveries"]) == 1
        assert result["invalid_deliveries"][0]["customer"] == "C"

    def test_transport_mode_selection(self):
        """Test transport mode options."""
        optimizer = CourierOptimizer()

        valid_modes = ["CAR", "BICYCLE", "WALKING"]
        for mode in valid_modes:
            assert optimizer.is_valid_transport_mode(mode) is True

        assert optimizer.is_valid_transport_mode("PLANE") is False
        assert optimizer.is_valid_transport_mode("TRAIN") is False

    def test_route_optimization_criteria(self):
        """Test route optimization criteria options."""
        optimizer = CourierOptimizer()

        valid_criteria = ["FASTEST", "CHEAPEST", "GREENEST"]
        for criteria in valid_criteria:
            assert optimizer.is_valid_optimization_criteria(criteria) is True

        assert optimizer.is_valid_optimization_criteria("SHORTEST") is False

    def test_distance_calculation(self):
        """Test distance calculation between two points."""
        optimizer = CourierOptimizer()

        # Oslo City Hall to Opera House (approximately 1.14 km)
        distance = optimizer.calculate_distance(59.9114, 10.7343, 59.9075, 10.7531)
        assert 1.0 < distance < 1.5

        # Same point should be 0 km
        distance_same = optimizer.calculate_distance(59.9, 10.75, 59.9, 10.75)
        assert distance_same == 0.0

    def test_travel_time_calculation(self):
        """Test travel time calculation for different transport modes."""
        optimizer = CourierOptimizer()

        distance = 10.0  # 10 km

        # Car: 50 km/h -> 10km = 0.2 hours
        time_car = optimizer.calculate_travel_time(distance, "CAR")
        assert time_car == 0.2

        # Bicycle: 15 km/h -> 10km = 0.667 hours
        time_bike = optimizer.calculate_travel_time(distance, "BICYCLE")
        assert abs(time_bike - 0.667) < 0.01

        # Walking: 5 km/h -> 10km = 2.0 hours
        time_walk = optimizer.calculate_travel_time(distance, "WALKING")
        assert time_walk == 2.0

    def test_cost_calculation(self):
        """Test cost calculation for different transport modes."""
        optimizer = CourierOptimizer()

        distance = 10.0  # 10 km

        # Car: 4 NOK/km -> 10km = 40 NOK
        cost_car = optimizer.calculate_cost(distance, "CAR")
        assert cost_car == 40.0

        # Bicycle: Free
        cost_bike = optimizer.calculate_cost(distance, "BICYCLE")
        assert cost_bike == 0.0

        # Walking: Free
        cost_walk = optimizer.calculate_cost(distance, "WALKING")
        assert cost_walk == 0.0

    def test_co2_calculation(self):
        """Test CO2 emissions calculation for different transport modes."""
        optimizer = CourierOptimizer()

        distance = 10.0  # 10 km

        # Car: 120 g/km -> 10km = 1200g
        co2_car = optimizer.calculate_co2(distance, "CAR")
        assert co2_car == 1200.0

        # Bicycle: Zero emissions
        co2_bike = optimizer.calculate_co2(distance, "BICYCLE")
        assert co2_bike == 0.0

        # Walking: Zero emissions
        co2_walk = optimizer.calculate_co2(distance, "WALKING")
        assert co2_walk == 0.0

    def test_route_optimization_by_priority(self):
        """Test that route optimization sorts by priority first."""
        optimizer = CourierOptimizer()

        deliveries = [
            {
                "customer": "Low Priority",
                "latitude": 59.91,
                "longitude": 10.74,
                "priority": "LOW",
                "weight_kg": 5,
            },
            {
                "customer": "High Priority",
                "latitude": 59.92,
                "longitude": 10.75,
                "priority": "HIGH",
                "weight_kg": 3,
            },
            {
                "customer": "Medium Priority",
                "latitude": 59.90,
                "longitude": 10.73,
                "priority": "MEDIUM",
                "weight_kg": 7,
            },
        ]

        route = optimizer.optimize_route(deliveries, "CAR", "FASTEST")

        # Check that HIGH comes first, then MEDIUM, then LOW
        assert route[0]["priority"] == "HIGH"
        assert route[1]["priority"] == "MEDIUM"
        assert route[2]["priority"] == "LOW"

    def test_route_optimization_empty_list(self):
        """Test route optimization with empty delivery list."""
        optimizer = CourierOptimizer()

        route = optimizer.optimize_route([], "CAR", "FASTEST")
        assert route == []

    def test_route_optimization_single_delivery(self):
        """Test route optimization with single delivery."""
        optimizer = CourierOptimizer()

        deliveries = [
            {
                "customer": "Only One",
                "latitude": 59.91,
                "longitude": 10.74,
                "priority": "HIGH",
                "weight_kg": 5,
            }
        ]

        route = optimizer.optimize_route(deliveries, "CAR", "FASTEST")
        assert len(route) == 1
        assert route[0]["customer"] == "Only One"
