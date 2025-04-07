using TotalSell.Domain.Common;
using TotalSell.Domain.Enums;

namespace TotalSell.Domain.Entities;

public abstract class Invoice : BaseEntity
{
    public required string Number { get; set; }
    public required DateTime Date { get; set; }
    public string? Description { get; protected set; }
    public decimal SubTotal { get; protected set; }
    public decimal TaxAmount { get; protected set; }
    public decimal DiscountAmount { get; protected set; }
    public decimal TotalAmount { get; protected set; }
    public string? PaymentTerms { get; protected set; }
    public required DateTime DueDate { get; set; }
    public required InvoiceStatus Status { get; set; }
    private readonly List<InvoiceItem> _items = new();
    public IReadOnlyCollection<InvoiceItem> Items => _items.AsReadOnly();

    protected Invoice() { } // For EF Core

    protected void Update(
        string number,
        DateTime date,
        string? description,
        string? paymentTerms,
        DateTime dueDate,
        InvoiceStatus status)
    {
        Number = number;
        Date = date;
        Description = description;
        PaymentTerms = paymentTerms;
        DueDate = dueDate;
        Status = status;
    }

    public void RemoveItem(InvoiceItem item)
    {
        _items.Remove(item);
        CalculateTotals();
        UpdatedAt = DateTime.UtcNow;
    }

    public void AddItem(InvoiceItem item)
    {
        _items.Add(item);
        CalculateTotals();
        UpdatedAt = DateTime.UtcNow;
    }

    private void CalculateTotals()
    {
        SubTotal = _items.Sum(x => x.Quantity * x.UnitPrice);
        TaxAmount = _items.Sum(x => x.TaxAmount);
        DiscountAmount = _items.Sum(x => x.DiscountAmount);
        TotalAmount = SubTotal + TaxAmount - DiscountAmount;
    }
} 