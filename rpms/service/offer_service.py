"""
OfferService - Business logic for job offers.
"""
from rpms.dao.offer_dao import OfferDAO
from rpms.dao.application_dao import ApplicationDAO
from rpms.model.offer import Offer
from rpms.exception.exceptions import OfferNotFoundError, ApplicationNotFoundError


class OfferService:

    def __init__(
        self,
        offer_dao: OfferDAO | None = None,
        application_dao: ApplicationDAO | None = None,
    ):
        self.offer_dao = offer_dao or OfferDAO()
        self.application_dao = application_dao or ApplicationDAO()

    def create_offer(self, offer: Offer) -> int:
        """Create a new job offer for a candidate application."""
        if not offer.application_id:
            raise ValueError("Application ID is required.")

        app = self.application_dao.find_by_id(offer.application_id)
        if not app:
            raise ApplicationNotFoundError(offer.application_id)

        if not offer.designation or not offer.designation.strip():
            raise ValueError("Designation cannot be empty.")

        if offer.offered_package_lpa <= 0:
            raise ValueError("Offered package must be greater than zero.")

        offer_id = self.offer_dao.save(offer)

        # Update application status to OFFERED
        self.application_dao.update_status(offer.application_id, "OFFERED")

        return offer_id

    def get_offer(self, offer_id: int) -> Offer:
        """Find offer by ID or raise OfferNotFoundError."""
        offer = self.offer_dao.find_by_id(offer_id)
        if not offer:
            raise OfferNotFoundError(offer_id)
        return offer

    def get_by_application(self, application_id: int) -> list[Offer]:
        """Return all offers for an application."""
        return self.offer_dao.find_by_application(application_id)

    def get_all_offers(self) -> list[Offer]:
        """Return all offers."""
        return self.offer_dao.find_all()

    def update_offer_status(self, offer_id: int, status: str) -> bool:
        """Update offer status (OFFERED/ACCEPTED/REJECTED/EXPIRED/WITHDRAWN)."""
        existing = self.offer_dao.find_by_id(offer_id)
        if not existing:
            raise OfferNotFoundError(offer_id)
        return self.offer_dao.update_status(offer_id, status.strip().upper())
