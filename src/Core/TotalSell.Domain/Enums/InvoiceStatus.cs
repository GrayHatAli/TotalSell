namespace TotalSell.Domain.Enums;

public enum InvoiceStatus
{
    Draft = 0,
    Pending = 1,
    Approved = 2,
    Rejected = 3,
    Cancelled = 4,
    Paid = 5,
    PartiallyPaid = 6,
    Overdue = 7,
    Void = 8
} 