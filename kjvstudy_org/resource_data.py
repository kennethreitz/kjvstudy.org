"""
Centralized data for theological resources.
This module provides data access for both listing and detail pages.
"""

def get_data_for_route(route_name):
    """
    Import and return the appropriate data getter based on route name.
    This avoids duplicating large data structures across routes.
    """
    # Import will happen dynamically based on route
    # For now, return None - routes will inline data until refactored
    return None
