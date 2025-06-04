from typing import TypeVar, Generic, List
from pydantic import BaseModel

from .user import User, UserCreate, UserUpdate, UserInDB
from .token import Token, TokenPayload
from .sales_channel import SalesChannel, SalesChannelCreate, SalesChannelUpdate
from .product import Product, ProductCreate, ProductUpdate
from .sales_order import SalesOrder, SalesOrderCreate, SalesOrderUpdate, SalesOrderItem, SalesOrderItemCreate
from .inventory import Inventory, InventoryCreate, InventoryUpdate, InventoryAlert, InventoryAlertCreate
from .supplier import Supplier, SupplierCreate, SupplierUpdate
from .logistics import LogisticsInformation, LogisticsInformationCreate, LogisticsInformationUpdate
from .communication import (
    Contact, ContactCreate, ContactUpdate, ContactListResponse,
    Message, MessageCreate, MessageUpdate,
    MessageTemplate, MessageTemplateCreate, MessageTemplateUpdate,
    QuickReply, QuickReplyCreate, QuickReplyUpdate,
    ChatSession
)

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    data: List[T]
    total: int
    message: str = ""

__all__ = [
    # API Response
    "APIResponse",
    # User schemas
    "User", "UserCreate", "UserUpdate", "UserInDB",
    # Token schemas
    "Token", "TokenPayload",
    # Sales channel schemas
    "SalesChannel", "SalesChannelCreate", "SalesChannelUpdate",
    # Product schemas
    "Product", "ProductCreate", "ProductUpdate",
    # Sales order schemas
    "SalesOrder", "SalesOrderCreate", "SalesOrderUpdate", "SalesOrderItem", "SalesOrderItemCreate",
    # Inventory schemas
    "Inventory", "InventoryCreate", "InventoryUpdate", "InventoryAlert", "InventoryAlertCreate",
    # Supplier schemas
    "Supplier", "SupplierCreate", "SupplierUpdate",
    # Logistics schemas
    "LogisticsInformation", "LogisticsInformationCreate", "LogisticsInformationUpdate",
    # Communication schemas
    "Contact", "ContactCreate", "ContactUpdate", "ContactListResponse",
    "Message", "MessageCreate", "MessageUpdate",
    "MessageTemplate", "MessageTemplateCreate", "MessageTemplateUpdate",
    "QuickReply", "QuickReplyCreate", "QuickReplyUpdate",
    "ChatSession"
] 