# import math
# import pandas as pd
# from sklearn.neighbors import NearestNeighbors
# from app.models import Donation, User

# def calculate_distance(lat1, lon1, lat2, lon2):
#     """
#     Calculate the Haversine distance between two points.
#     """
#     # Convert decimal degrees to radians
#     lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
#     # Haversine formula
#     dlat = lat2 - lat1 
#     dlon = lon2 - lon1 
#     a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
#     c = 2 * math.asin(math.sqrt(a))
#     r = 6371  # Radius of earth in kilometers
#     return c * r

# def match_donations():
#     """
#     Matches each donation to the nearest NGO using latitude and longitude.
#     """
#     donations = Donation.query.all()
#     ngos = User.query.filter_by(role="NGO").all()

#     if not donations or not ngos:
#         return []

#     matches = []
#     for donation in donations:
#         try:
#             d_lat = float(donation.latitude)
#             d_lon = float(donation.longitude)
#         except (TypeError, ValueError):
#             continue  # Skip if donation doesn't have valid coordinates

#         best_match = None
#         min_distance = float("inf")
#         for ngo in ngos:
#             # Assuming NGOs would have stored latitude and longitude similarly.
#             if hasattr(ngo, 'latitude') and hasattr(ngo, 'longitude') and ngo.latitude and ngo.longitude:
#                 try:
#                     n_lat = float(ngo.latitude)
#                     n_lon = float(ngo.longitude)
#                     distance = calculate_distance(d_lat, d_lon, n_lat, n_lon)
#                     if distance < min_distance:
#                         min_distance = distance
#                         best_match = ngo
#                 except (TypeError, ValueError):
#                     continue
#         matches.append((donation.id, best_match.id if best_match else None))
#     return matches
import math
from app.models import Donation, User

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the Haversine distance between two points on the Earth (in kilometers).
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of Earth in kilometers.
    return c * r

def get_nearest_ngo(donation, ngo_list):
    """
    Given a donation and a list of NGOs, return the NGO with the minimum distance.
    Assumes both donation and NGO have valid latitude and longitude values.
    """
    try:
        d_lat = float(donation.latitude)
        d_lon = float(donation.longitude)
    except (TypeError, ValueError):
        return None

    best_match = None
    min_distance = float("inf")
    for ngo in ngo_list:
        if hasattr(ngo, 'latitude') and hasattr(ngo, 'longitude') and ngo.latitude and ngo.longitude:
            try:
                n_lat = float(ngo.latitude)
                n_lon = float(ngo.longitude)
                distance = calculate_distance(d_lat, d_lon, n_lat, n_lon)
                if distance < min_distance:
                    min_distance = distance
                    best_match = ngo
            except (TypeError, ValueError):
                continue
    return best_match

def match_donations():
    """
    Matches each donation to the nearest NGO using latitude and longitude.
    Returns a list of tuples: (donation_id, nearest_ngo_id).
    """
    donations = Donation.query.all()
    ngos = User.query.filter_by(role="NGO").all()

    if not donations or not ngos:
        return []

    matches = []
    for donation in donations:
        nearest_ngo = get_nearest_ngo(donation, ngos)
        matches.append((donation.id, nearest_ngo.id if nearest_ngo else None))
    return matches
