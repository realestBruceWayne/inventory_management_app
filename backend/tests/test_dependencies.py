import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dependencies import (
    get_product_repository,
    get_customer_repository,
    get_order_repository,
    get_product_service,
    get_customer_service,
    get_order_service
)
from repositories.sqlalchemy_repositories import (
    SQLAlchemyProductRepository,
    SQLAlchemyCustomerRepository,
    SQLAlchemyOrderRepository
)
from services.product_service import ProductService
from services.customer_service import CustomerService
from services.order_service import OrderService


class TestProductRepositoryDependency:
    """Test suite for product repository dependency"""

    @patch('dependencies.get_db')
    def test_get_product_repository(self, mock_get_db):
        """Test getting product repository"""
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        repo = get_product_repository(mock_db)
        
        assert isinstance(repo, SQLAlchemyProductRepository)
        mock_get_db.assert_called_once()

    @patch('dependencies.get_db')
    def test_get_product_repository_with_session(self, mock_get_db):
        """Test getting product repository with database session"""
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        repo = get_product_repository(mock_db)
        
        assert repo.db == mock_db


class TestCustomerRepositoryDependency:
    """Test suite for customer repository dependency"""

    @patch('dependencies.get_db')
    def test_get_customer_repository(self, mock_get_db):
        """Test getting customer repository"""
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        repo = get_customer_repository(mock_db)
        
        assert isinstance(repo, SQLAlchemyCustomerRepository)
        mock_get_db.assert_called_once()

    @patch('dependencies.get_db')
    def test_get_customer_repository_with_session(self, mock_get_db):
        """Test getting customer repository with database session"""
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        repo = get_customer_repository(mock_db)
        
        assert repo.db == mock_db


class TestOrderRepositoryDependency:
    """Test suite for order repository dependency"""

    @patch('dependencies.get_db')
    def test_get_order_repository(self, mock_get_db):
        """Test getting order repository"""
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        repo = get_order_repository(mock_db)
        
        assert isinstance(repo, SQLAlchemyOrderRepository)
        mock_get_db.assert_called_once()

    @patch('dependencies.get_db')
    def test_get_order_repository_with_session(self, mock_get_db):
        """Test getting order repository with database session"""
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        repo = get_order_repository(mock_db)
        
        assert repo.db == mock_db


class TestProductServiceDependency:
    """Test suite for product service dependency"""

    @patch('dependencies.get_product_repository')
    def test_get_product_service(self, mock_get_repo):
        """Test getting product service"""
        mock_repo = Mock()
        mock_get_repo.return_value = mock_repo
        
        service = get_product_service(mock_repo)
        
        assert isinstance(service, ProductService)
        assert service.product_repository == mock_repo
        mock_get_repo.assert_called_once()


class TestCustomerServiceDependency:
    """Test suite for customer service dependency"""

    @patch('dependencies.get_customer_repository')
    def test_get_customer_service(self, mock_get_repo):
        """Test getting customer service"""
        mock_repo = Mock()
        mock_get_repo.return_value = mock_repo
        
        service = get_customer_service(mock_repo)
        
        assert isinstance(service, CustomerService)
        assert service.customer_repository == mock_repo
        mock_get_repo.assert_called_once()


class TestOrderServiceDependency:
    """Test suite for order service dependency"""

    @patch('dependencies.get_order_repository')
    @patch('dependencies.get_product_repository')
    @patch('dependencies.get_customer_repository')
    def test_get_order_service(self, mock_customer_repo, mock_product_repo, mock_order_repo):
        """Test getting order service"""
        mock_order_repo_instance = Mock()
        mock_product_repo_instance = Mock()
        mock_customer_repo_instance = Mock()
        
        mock_order_repo.return_value = mock_order_repo_instance
        mock_product_repo.return_value = mock_product_repo_instance
        mock_customer_repo.return_value = mock_customer_repo_instance
        
        service = get_order_service(
            mock_order_repo_instance,
            mock_product_repo_instance,
            mock_customer_repo_instance
        )
        
        assert isinstance(service, OrderService)
        assert service.order_repository == mock_order_repo_instance
        assert service.product_repository == mock_product_repo_instance
        assert service.customer_repository == mock_customer_repo_instance


class TestDependencyIntegration:
    """Test suite for dependency integration"""

    @patch('dependencies.get_product_repository')
    @patch('dependencies.get_customer_repository')
    @patch('dependencies.get_order_repository')
    @patch('dependencies.get_db')
    def test_full_dependency_chain(self, mock_get_db, mock_order_repo, mock_customer_repo, mock_product_repo):
        """Test full dependency chain"""
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Test repository dependencies
        product_repo = get_product_repository(mock_db)
        customer_repo = get_customer_repository(mock_db)
        order_repo = get_order_repository(mock_db)
        
        assert isinstance(product_repo, SQLAlchemyProductRepository)
        assert isinstance(customer_repo, SQLAlchemyCustomerRepository)
        assert isinstance(order_repo, SQLAlchemyOrderRepository)
        
        # Test service dependencies
        product_service = get_product_service(product_repo)
        customer_service = get_customer_service(customer_repo)
        order_service = get_order_service(order_repo, product_repo, customer_repo)
        
        assert isinstance(product_service, ProductService)
        assert isinstance(customer_service, CustomerService)
        assert isinstance(order_service, OrderService)