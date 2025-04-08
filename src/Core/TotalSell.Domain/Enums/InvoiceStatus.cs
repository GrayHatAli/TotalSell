namespace TotalSell.Domain.Enums;

public enum InvoiceStatus
{
    Draft = 1,
    Pending = 2,
    Approved = 3,
    Rejected = 4,
    Cancelled = 5,
    Paid = 6,
    PartiallyPaid = 7,
    Overdue = 8,
    Void = 9
} 