from typing import Dict, List, Any


class CourierOptimizer:
    """
    Main courier optimization system for Oslo's NordicExpress service. """
    
    # Oslo geographic bounds - these define our service area
    # Real Oslo coordinates (approximately)
    OSLO_LAT_MIN = 59.8  # Southern boundary
    OSLO_LAT_MAX = 60.0  # Northern boundary
    OSLO_LON_MIN = 10.6  # Western boundary  
    OSLO_LON_MAX = 10.9  # Eastern boundary
    
    # Business rules from assignment requirements
    VALID_PRIORITIES = {'HIGH', 'MEDIUM', 'LOW'}
    VALID_TRANSPORT_MODES = {'CAR', 'BICYCLE', 'WALKING'}
    VALID_OPTIMIZATION_CRITERIA = {'FASTEST', 'CHEAPEST', 'GREENEST'}
    
    # Physical constraints
    MAX_WEIGHT_KG = 25.0  # Maximum package weight
    
    def __init__(self):
        """
        Initialize CourierOptimizer with empty state.
        """
        self.current_deliveries = []
        self.last_optimization_result = None
    
    def _validate_weight(self, weight: float) -> List[str]:
        """
        Validate package weight against business rules.
        """
        warnings = []
        
        if weight > self.MAX_WEIGHT_KG:
            warnings.append(f"Weight {weight}kg exceeds maximum {self.MAX_WEIGHT_KG}kg")
        
        if weight < 0:
            warnings.append(f"Weight cannot be negative: {weight}kg")
            
        return warnings
    
    def _validate_priority(self, priority: str) -> List[str]:
        """
        Validate priority level against allowed values.
        
        Args:
            priority: Priority string (case-insensitive)
            
        Returns:
            List of warning messages (empty if valid)
        """
        warnings = []
        priority_upper = priority.upper() if priority else ''
        
        if priority_upper not in self.VALID_PRIORITIES:
            valid_options = ', '.join(self.VALID_PRIORITIES)
            warnings.append(f"Invalid priority '{priority}'. Must be: {valid_options}")
            
        return warnings
    
    def _validate_coordinates(self, latitude: float, longitude: float) -> List[str]:
        """
        Validate coordinates are within Oslo service area.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            List of warning messages (empty if valid)
            
         Note: Check if coordinates fall within Oslo's boundaries.
        If outside, the delivery can't be serviced.
        """
        warnings = []
        
        # Check latitude bounds (North-South position)
        if not (self.OSLO_LAT_MIN <= latitude <= self.OSLO_LAT_MAX):
            warnings.append(
                f"Latitude {latitude} outside Oslo bounds "
                f"({self.OSLO_LAT_MIN}-{self.OSLO_LAT_MAX})"
            )
        
        # Check longitude bounds (East-West position)  
        if not (self.OSLO_LON_MIN <= longitude <= self.OSLO_LON_MAX):
            warnings.append(
                f"Longitude {longitude} outside Oslo bounds "
                f"({self.OSLO_LON_MIN}-{self.OSLO_LON_MAX})"
            )
            
        return warnings
    
    def _validate_customer_name(self, customer: str) -> List[str]:
        """
        Validate customer name is present and printable.
        
        Args:
            customer: Customer name string
            
        Returns:
            List of warning messages (empty if valid)
        """
        warnings = []
        
        if not customer or not customer.strip():
            warnings.append("Customer name cannot be empty")
        elif len(customer.strip()) < 2:
            warnings.append("Customer name too short (minimum 2 characters)")
            
        return warnings

    def validate_delivery(self, delivery: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a single delivery entry against business requirements.
        
        Args:
            delivery: Dict with keys: customer, latitude, longitude, priority, weight_kg
            
        Returns:
            Dict with 'is_valid' (bool) and 'warnings' (list of str)
        """
        all_warnings = []
        
        # Use all validation helpers to collect warnings
        all_warnings.extend(self._validate_weight(delivery.get('weight_kg', 0)))
        all_warnings.extend(self._validate_priority(delivery.get('priority', '')))
        all_warnings.extend(self._validate_coordinates(
            delivery.get('latitude', 0), 
            delivery.get('longitude', 0)
        ))
        all_warnings.extend(self._validate_customer_name(delivery.get('customer', '')))
        
        return {
            'is_valid': len(all_warnings) == 0,
            'warnings': all_warnings
        }
    
    def process_csv_data(self, data) -> Dict[str, List[Dict]]:
        """
        Process CSV data and separate valid from invalid deliveries.
        
        Args:
            data: DataFrame with delivery data
            
        Returns:
            Dict with 'valid_deliveries' and 'invalid_deliveries' lists
        """
        return {'valid_deliveries': [], 'invalid_deliveries': []}
    
    def is_valid_transport_mode(self, mode: str) -> bool:
        """Check if transport mode is valid."""
        return mode.upper() in self.VALID_TRANSPORT_MODES
    
    def is_valid_optimization_criteria(self, criteria: str) -> bool:
        """Check if optimization criteria is valid."""
        return criteria.upper() in self.VALID_OPTIMIZATION_CRITERIA
    
    def optimize_route(self, deliveries: List[Dict], transport_mode: str, 
                      criteria: str) -> List[Dict]:
        """
        Optimize delivery route based on specified criteria.
        
        Args:
            deliveries: List of valid delivery dictionaries
            transport_mode: 'CAR', 'BICYCLE', or 'WALKING'  
            criteria: 'FASTEST', 'CHEAPEST', or 'GREENEST'
            
        Returns:
            List of deliveries in optimized order
        """
        return deliveries.copy() if deliveries else []