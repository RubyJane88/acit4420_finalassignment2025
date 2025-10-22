from typing import Dict, List, Any
import pandas as pd
from geopy.distance import geodesic


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
    
    # Transport mode parameters (speed in km/h, cost in NOK/km, CO2 in g/km)
    TRANSPORT_PARAMS = {
        'CAR': {
            'speed_kmh': 50,
            'cost_per_km': 4.0,
            'co2_g_per_km': 120
        },
        'BICYCLE': {
            'speed_kmh': 15,
            'cost_per_km': 0.0,
            'co2_g_per_km': 0
        },
        'WALKING': {
            'speed_kmh': 5,
            'cost_per_km': 0.0,
            'co2_g_per_km': 0
        }
    }
    
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
        elif len(customer.strip()) < 1:
            warnings.append("Customer name cannot be empty")
            
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
        valid_deliveries = []
        invalid_deliveries = []
        
        for _, row in data.iterrows():
            delivery = row.to_dict()
            validation_result = self.validate_delivery(delivery)
            
            if validation_result['is_valid']:
                valid_deliveries.append(delivery)
            else:
                # Add warnings to the delivery record for output
                delivery['warnings'] = validation_result['warnings']
                invalid_deliveries.append(delivery)
        
        return {
            'valid_deliveries': valid_deliveries,
            'invalid_deliveries': invalid_deliveries
        }
    
    def is_valid_transport_mode(self, mode: str) -> bool:
        """Check if transport mode is valid."""
        return mode.upper() in self.VALID_TRANSPORT_MODES
    
    def is_valid_optimization_criteria(self, criteria: str) -> bool:
        """Check if optimization criteria is valid."""
        return criteria.upper() in self.VALID_OPTIMIZATION_CRITERIA
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two GPS coordinates.
        
        Uses geopy's geodesic calculation for more accurate distance measurements
        
        Args:
            lat1: Latitude of first point
            lon1: Longitude of first point
            lat2: Latitude of second point
            lon2: Longitude of second point
            
        Returns:
            Distance in kilometers
        """
        point1 = (lat1, lon1)
        point2 = (lat2, lon2)
        return geodesic(point1, point2).kilometers
    
    def calculate_travel_time(self, distance_km: float, transport_mode: str) -> float:
        """
        Calculate travel time in hours for a given distance and transport mode.
        
        Args:
            distance_km: Distance in kilometers
            transport_mode: Transport mode (CAR, BICYCLE, WALKING)
            
        Returns:
            Travel time in hours
        """
        mode = transport_mode.upper()
        if mode not in self.TRANSPORT_PARAMS:
            raise ValueError(f"Invalid transport mode: {transport_mode}")
        
        speed = self.TRANSPORT_PARAMS[mode]['speed_kmh']
        return distance_km / speed
    
    def calculate_cost(self, distance_km: float, transport_mode: str) -> float:
        """
        Calculate cost in NOK for a given distance and transport mode.
        
        Args:
            distance_km: Distance in kilometers
            transport_mode: Transport mode (CAR, BICYCLE, WALKING)
            
        Returns:
            Cost in NOK
        """
        mode = transport_mode.upper()
        if mode not in self.TRANSPORT_PARAMS:
            raise ValueError(f"Invalid transport mode: {transport_mode}")
        
        cost_per_km = self.TRANSPORT_PARAMS[mode]['cost_per_km']
        return distance_km * cost_per_km
    
    def calculate_co2(self, distance_km: float, transport_mode: str) -> float:
        """
        Calculate CO2 emissions in grams for a given distance and transport mode.
        
        Args:
            distance_km: Distance in kilometers
            transport_mode: Transport mode (CAR, BICYCLE, WALKING)
            
        Returns:
            CO2 emissions in grams
        """
        mode = transport_mode.upper()
        if mode not in self.TRANSPORT_PARAMS:
            raise ValueError(f"Invalid transport mode: {transport_mode}")
        
        co2_per_km = self.TRANSPORT_PARAMS[mode]['co2_g_per_km']
        return distance_km * co2_per_km
    
    def optimize_route(self, deliveries: List[Dict], transport_mode: str, 
                      criteria: str) -> List[Dict]:
        """
        Optimize delivery route by sorting based on priority and proximity.
        
        Sort by priority first (HIGH > MEDIUM > LOW),
        then by distance from depot for deliveries with same priority.
        
        Args:
            deliveries: List of valid delivery dictionaries
            transport_mode: 'CAR', 'BICYCLE', or 'WALKING'  
            criteria: 'FASTEST', 'CHEAPEST', or 'GREENEST'
            
        Returns:
            List of deliveries in optimized order
        """
        if not deliveries:
            return []
        
        if len(deliveries) == 1:
            return deliveries.copy()
        
        # Depot location (Oslo City Hall)
        depot_lat = 59.9114
        depot_lon = 10.7343
        
        # Priority ranking for sorting
        priority_rank = {'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        
        # Sort by priority first, then by distance from depot
        sorted_deliveries = sorted(
            deliveries,
            key=lambda d: (
                priority_rank.get(d.get('priority', 'LOW').upper(), 3),
                self.calculate_distance(depot_lat, depot_lon, 
                                       d['latitude'], d['longitude'])
            )
        )
        
        return sorted_deliveries
    
    def calculate_route_metrics(self, route: List[Dict], transport_mode: str) -> Dict[str, float]:
        """
        Calculate total metrics for a delivery route.
        
        Calculates the total distance, time, cost, and CO2 emissions for traveling
        the entire route from depot through all deliveries and back to depot.
        
        Args:
            route: List of delivery dictionaries in route order
            transport_mode: Transport mode to use (CAR, BICYCLE, WALKING)
            
        Returns:
            Dictionary containing:
                - total_distance_km: Total distance in kilometers
                - total_time_hours: Total travel time in hours
                - total_cost_nok: Total cost in Norwegian Kroner
                - total_co2_grams: Total CO2 emissions in grams
        """
        if not route:
            return {
                'total_distance_km': 0.0,
                'total_time_hours': 0.0,
                'total_cost_nok': 0.0,
                'total_co2_grams': 0.0
            }
        
        # Depot location (Oslo City Hall)
        depot_lat = 59.9114
        depot_lon = 10.7343
        
        total_distance = 0.0
        current_lat = depot_lat
        current_lon = depot_lon
        
        # Calculate distance through all deliveries
        for delivery in route:
            distance = self.calculate_distance(
                current_lat, current_lon,
                delivery['latitude'], delivery['longitude']
            )
            total_distance += distance
            current_lat = delivery['latitude']
            current_lon = delivery['longitude']
        
        # Return to depot
        distance_back = self.calculate_distance(
            current_lat, current_lon,
            depot_lat, depot_lon
        )
        total_distance += distance_back
        
        # Calculate metrics based on total distance
        total_time = self.calculate_travel_time(total_distance, transport_mode)
        total_cost = self.calculate_cost(total_distance, transport_mode)
        total_co2 = self.calculate_co2(total_distance, transport_mode)
        
        return {
            'total_distance_km': round(total_distance, 2),
            'total_time_hours': round(total_time, 2),
            'total_cost_nok': round(total_cost, 2),
            'total_co2_grams': round(total_co2, 2)
        }
    
    def read_deliveries_csv(self, filepath: str) -> pd.DataFrame:
        """
        Read deliveries from CSV file.
        
        Args:
            filepath: Path to deliveries CSV file
            
        Returns:
            DataFrame with delivery data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If CSV has invalid format
        """
        try:
            df = pd.read_csv(filepath)
            
            # Check required columns
            required_columns = {'customer', 'latitude', 'longitude', 'priority', 'weight_kg'}
            missing_columns = required_columns - set(df.columns)
            
            if missing_columns:
                raise ValueError(f"CSV missing required columns: {missing_columns}")
            
            return df
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Deliveries file not found: {filepath}")
        except pd.errors.EmptyDataError:
            raise ValueError(f"CSV file is empty: {filepath}")
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {str(e)}")
    
    def write_route_csv(self, route: List[Dict], metrics: Dict[str, float], 
                       filepath: str, transport_mode: str) -> None:
        """
        Write optimized route to CSV file with detailed metrics.
        
        Args:
            route: List of deliveries in optimized order
            metrics: Dictionary with total route metrics
            filepath: Output CSV file path
            transport_mode: Transport mode used
        """
        if not route:
            # Write empty file with headers only
            df = pd.DataFrame(columns=['stop_number', 'customer', 'latitude', 'longitude', 
                                      'priority', 'weight_kg', 'distance_km', 'cumulative_distance_km',
                                      'eta_hours', 'cost_nok', 'co2_grams'])
            df.to_csv(filepath, index=False)
            return
        
        # Depot location
        depot_lat = 59.9114
        depot_lon = 10.7343
        
        # Build route data with cumulative metrics
        route_data = []
        cumulative_distance = 0.0
        prev_lat, prev_lon = depot_lat, depot_lon
        
        for i, delivery in enumerate(route, 1):
            # Distance from previous point
            segment_distance = self.calculate_distance(
                prev_lat, prev_lon,
                delivery['latitude'], delivery['longitude']
            )
            cumulative_distance += segment_distance
            
            # Calculate segment metrics
            segment_time = self.calculate_travel_time(segment_distance, transport_mode)
            segment_cost = self.calculate_cost(segment_distance, transport_mode)
            segment_co2 = self.calculate_co2(segment_distance, transport_mode)
            
            route_data.append({
                'stop_number': i,
                'customer': delivery['customer'],
                'latitude': delivery['latitude'],
                'longitude': delivery['longitude'],
                'priority': delivery['priority'],
                'weight_kg': delivery['weight_kg'],
                'distance_km': round(segment_distance, 2),
                'cumulative_distance_km': round(cumulative_distance, 2),
                'eta_hours': round(segment_time, 2),
                'cost_nok': round(segment_cost, 2),
                'co2_grams': round(segment_co2, 2)
            })
            
            prev_lat, prev_lon = delivery['latitude'], delivery['longitude']
        
        # Create DataFrame and save
        df = pd.DataFrame(route_data)
        df.to_csv(filepath, index=False)
        
        print(f"\n✅ Route saved to: {filepath}")
        print(f"   Transport mode: {transport_mode}")
        print(f"   Total stops: {len(route)}")
        print(f"   Total distance: {metrics['total_distance_km']} km")
        print(f"   Total time: {metrics['total_time_hours']} hours ({metrics['total_time_hours']*60:.0f} minutes)")
        print(f"   Total cost: {metrics['total_cost_nok']} NOK")
        print(f"   Total CO2: {metrics['total_co2_grams']} grams ({metrics['total_co2_grams']/1000:.2f} kg)")
    
    def write_rejected_csv(self, invalid_deliveries: List[Dict], filepath: str) -> None:
        """
        Write rejected deliveries to CSV file with warning messages.
        
        Args:
            invalid_deliveries: List of invalid delivery dictionaries with warnings
            filepath: Output CSV file path
        """
        if not invalid_deliveries:
            # Write empty file with headers
            df = pd.DataFrame(columns=['customer', 'latitude', 'longitude', 
                                      'priority', 'weight_kg', 'warnings'])
            df.to_csv(filepath, index=False)
            print(f"\n✅ No rejected deliveries")
            return
        
        # Prepare data with warnings as string
        rejected_data = []
        for delivery in invalid_deliveries:
            rejected_data.append({
                'customer': delivery.get('customer', ''),
                'latitude': delivery.get('latitude', ''),
                'longitude': delivery.get('longitude', ''),
                'priority': delivery.get('priority', ''),
                'weight_kg': delivery.get('weight_kg', ''),
                'warnings': ' | '.join(delivery.get('warnings', []))
            })
        
        df = pd.DataFrame(rejected_data)
        df.to_csv(filepath, index=False)
        
        print(f"\n⚠️  Rejected deliveries saved to: {filepath}")
        print(f"   Total rejected: {len(invalid_deliveries)}")
