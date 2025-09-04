from app.db.base import BaseModel


class Listing(BaseModel):
    def __init__(
        self,
        id,
        name,
        host_id,
        host_name,
        neighbourhood_group,
        neighbourhood,
        latitude,
        longitude,
        room_type,
        price,
        minimum_nights,
        number_of_reviews,
        last_review,
        reviews_per_month,
        calculated_host_listings_count,
        availability_365,
    ):
        self.id = id
        self.name = name
        self.host_id = host_id
        self.host_name = host_name
        self.neighbourhood_group = neighbourhood_group
        self.neighbourhood = neighbourhood
        self.latitude = latitude
        self.longitude = longitude
        self.room_type = room_type
        self.price = price
        self.minimum_nights = minimum_nights
        self.number_of_reviews = number_of_reviews
        self.last_review = last_review
        self.reviews_per_month = reviews_per_month
        self.calculated_host_listings_count = calculated_host_listings_count
        self.availability_365 = availability_365
