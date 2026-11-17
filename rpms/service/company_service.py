"""
CompanyService - Business logic for company operations.
"""
from rpms.dao.company_dao import CompanyDAO
from rpms.model.company import Company
from rpms.exception.exceptions import CompanyNotFoundError


class CompanyService:

    def __init__(self, company_dao: CompanyDAO | None = None):
        self.company_dao = company_dao or CompanyDAO()

    def add_company(self, company: Company) -> int:
        """Validate and add a new company."""
        if not company.company_name or not company.company_name.strip():
            raise ValueError("Company name cannot be empty.")
        company.company_name = company.company_name.strip()
        return self.company_dao.save(company)

    def get_company(self, company_id: int) -> Company:
        """Find company by ID or raise CompanyNotFoundError."""
        company = self.company_dao.find_by_id(company_id)
        if not company:
            raise CompanyNotFoundError(company_id)
        return company

    def get_all_companies(self) -> list[Company]:
        """Return all companies."""
        return self.company_dao.find_all()

    def search_by_name(self, name: str) -> list[Company]:
        """Search companies by name."""
        return self.company_dao.find_by_name(name.strip())

    def update_company(self, company: Company) -> bool:
        """Update company details."""
        if not company.company_id:
            raise ValueError("Company ID required for update.")
        existing = self.company_dao.find_by_id(company.company_id)
        if not existing:
            raise CompanyNotFoundError(company.company_id)
        return self.company_dao.update(company)

    def update_status(self, company_id: int, status: str) -> bool:
        """Update company status (ACTIVE/INACTIVE)."""
        existing = self.company_dao.find_by_id(company_id)
        if not existing:
            raise CompanyNotFoundError(company_id)
        return self.company_dao.update_status(company_id, status.strip().upper())
