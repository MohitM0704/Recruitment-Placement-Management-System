"""
PlacementService - Business logic for placement confirmation and tracking.
"""
from rpms.dao.placement_dao import PlacementDAO
from rpms.dao.candidate_dao import CandidateDAO
from rpms.dao.offer_dao import OfferDAO
from rpms.dao.application_dao import ApplicationDAO
from rpms.model.placement import Placement
from rpms.exception.exceptions import (
    PlacementNotFoundError,
    CandidateNotFoundError,
    OfferNotFoundError,
)


class PlacementService:

    def __init__(
        self,
        placement_dao: PlacementDAO | None = None,
        candidate_dao: CandidateDAO | None = None,
        offer_dao: OfferDAO | None = None,
        application_dao: ApplicationDAO | None = None,
    ):
        self.placement_dao = placement_dao or PlacementDAO()
        self.candidate_dao = candidate_dao or CandidateDAO()
        self.offer_dao = offer_dao or OfferDAO()
        self.application_dao = application_dao or ApplicationDAO()

    def confirm_placement(self, placement: Placement) -> int:
        """
        Record a placement / joining confirmation.
        When joining_status == 'JOINED':
          - Update candidate placement_status to 'PLACED'
          - Update offer status to 'ACCEPTED'
          - Update application status to 'JOINED'
        """
        if not placement.candidate_id:
            raise ValueError("Candidate ID is required.")

        candidate = self.candidate_dao.find_by_id(placement.candidate_id)
        if not candidate:
            raise CandidateNotFoundError(placement.candidate_id)

        if not placement.offer_id:
            raise ValueError("Offer ID is required.")

        offer = self.offer_dao.find_by_id(placement.offer_id)
        if not offer:
            raise OfferNotFoundError(placement.offer_id)

        placement_id = self.placement_dao.save(placement)

        # Handle joining updates
        if placement.joining_status.upper() == "JOINED":
            self.candidate_dao.update_placement_status(placement.candidate_id, "PLACED")
            self.offer_dao.update_status(placement.offer_id, "ACCEPTED")
            if offer.application_id:
                self.application_dao.update_status(offer.application_id, "JOINED")

        return placement_id

    def get_placement(self, placement_id: int) -> Placement:
        """Find placement by ID or raise PlacementNotFoundError."""
        placement = self.placement_dao.find_by_id(placement_id)
        if not placement:
            raise PlacementNotFoundError(placement_id)
        return placement

    def get_by_candidate(self, candidate_id: int) -> list[Placement]:
        """Return all placements for a candidate."""
        return self.placement_dao.find_by_candidate(candidate_id)

    def get_all_joined(self) -> list[Placement]:
        """Return all confirmed (JOINED) placements."""
        return self.placement_dao.find_all_joined()

    def get_all_placements(self) -> list[Placement]:
        """Return all placements."""
        return self.placement_dao.find_all()
