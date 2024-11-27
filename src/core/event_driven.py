from collections import defaultdict
import uuid

class Event:
    """Base class for all events."""
    def __init__(self, event_type, data=None):
        self.event_type = event_type
        self.data = data or {}
        self.event_id = str(uuid.uuid4())  # Unique identifier for the event

class EventBus:
    """Event bus for managing event listeners and dispatching events."""
    def __init__(self):
        self.listeners = defaultdict(list)

    def subscribe(self, event_type, listener):
        """Subscribe a listener to an event type."""
        self.listeners[event_type].append(listener)

    def unsubscribe(self, event_type, listener):
        """Unsubscribe a listener from an event type."""
        if listener in self.listeners[event_type]:
            self.listeners[event_type].remove(listener)

    def publish(self, event):
        """Publish an event to all subscribed listeners."""
        for listener in self.listeners.get(event.event_type, []):
            listener(event)

class TransactionCreatedEvent(Event):
    """Event triggered when a transaction is created."""
    def __init__(self, transaction):
        super().__init__('transaction_created', {'transaction': transaction})

class TransactionExecutedEvent(Event):
    """Event triggered when a transaction is executed."""
    def __init__(self, transaction):
        super().__init__('transaction_executed', {'transaction': transaction})

class TransactionFailedEvent(Event):
    """Event triggered when a transaction fails."""
    def __init__(self, transaction):
        super().__init__('transaction_failed', {'transaction': transaction})

class EventListener:
    """Base class for event listeners."""
    def handle_event(self, event):
        raise NotImplementedError("Event handler must be implemented.")

class TransactionLogger(EventListener):
    """Listener that logs transaction events."""
    def handle_event(self, event):
        if event.event_type == 'transaction_created':
            print(f"Transaction created: {event.data['transaction']}")
        elif event.event_type == 'transaction_executed':
            print(f"Transaction executed: {event.data['transaction']}")
        elif event.event_type == 'transaction_failed':
            print(f"Transaction failed: {event.data['transaction']}")

class TransactionProcessor:
    """Class that processes transactions and triggers events."""
    def __init__(self, event_bus):
        self.event_bus = event_bus

    def create_transaction(self, transaction):
        # Simulate transaction creation logic
        self.event_bus.publish(TransactionCreatedEvent(transaction))

    def execute_transaction(self, transaction):
        # Simulate transaction execution logic
        success = True  # Simulate success or failure
        if success:
            self.event_bus.publish(TransactionExecutedEvent(transaction))
        else:
            self.event_bus.publish(TransactionFailedEvent(transaction))

# Example usage
if __name__ == "__main__":
    event_bus = EventBus()
    logger = TransactionLogger()
    event_bus.subscribe('transaction_created', logger.handle_event)
    event_bus.subscribe('transaction_executed', logger.handle_event)
    event_bus.subscribe('transaction_failed', logger.handle_event)

    processor = TransactionProcessor(event_bus)

    # Create and execute a transaction
    transaction = {"id": "tx1", "amount": 100, "sender": "0x123", "recipient": "0x456"}
    processor.create_transaction(transaction)
    processor.execute_transaction(transaction)
