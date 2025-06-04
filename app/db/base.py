# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.sales_channel import SalesChannel  # noqa
from app.models.sales_order import SalesOrder, SalesOrderItem  # noqa
from app.models.product import Product  # noqa
from app.models.inventory import Inventory, InventoryAlert  # noqa
from app.models.supplier import Supplier  # noqa
from app.models.synced_order import SyncedChannelOrder, SyncedChannelOrderItem  # noqa
from app.models.order_sync_log import OrderSyncLog  # noqa
from app.models.communication import CommunicationMessage  # noqa
from app.models.logistics import LogisticsInformation  # noqa 