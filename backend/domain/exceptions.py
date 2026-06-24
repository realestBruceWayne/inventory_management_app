class DomainException(Exception):
    """Base exception for domain-specific errors"""
    pass


class ProductNotFoundException(DomainException):
    """Raised when a product is not found"""
    pass


class ProductSKUAlreadyExistsException(DomainException):
    """Raised when attempting to create a product with an existing SKU"""
    pass


class CustomerNotFoundException(DomainException):
    """Raised when a customer is not found"""
    pass


class CustomerEmailAlreadyExistsException(DomainException):
    """Raised when attempting to create a customer with an existing email"""
    pass


class OrderNotFoundException(DomainException):
    """Raised when an order is not found"""
    pass


class InsufficientInventoryException(DomainException):
    """Raised when there is insufficient inventory for an order"""
    pass
