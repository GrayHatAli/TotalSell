using TotalSell.Domain.Common;
using TotalSell.Domain.Enums;

namespace TotalSell.Domain.Entities;

public abstract class Invoice : BaseEntity
{
    public required string Number { get; set; }
    public required DateTime Date { get; set; }
    public string? Description { get; set; }
    public decimal SubTotal { get; protected set; }
    public decimal TaxAmount { get; protected set; }
    public decimal DiscountAmount { get; protected set; }
    public decimal TotalAmount { get; protected set; }
    public required DateTime DueDate { get; set; }
    public required InvoiceStatus Status { get; set; }
    public required InvoiceType Type { get; set; }
    public virtual required Guid CustomerId { get; set; }
    public virtual required Customer Customer { get; set; }
    public virtual string? ReferenceNumber { get; set; }
    public virtual DateTime? ReferenceDate { get; set; }
    public virtual string? PaymentMethod { get; set; }
    public List<InvoiceItem> Items { get; protected set; } = new();

    protected Invoice() { } // For EF Core

    public virtual void Update(
        string number,
        DateTime date,
        string? description,
        DateTime dueDate,
        InvoiceStatus status,
        Guid customerId,
        Customer customer,
        string? referenceNumber,
        DateTime? referenceDate,
        string? paymentMethod)
    {
        Number = number;
        Date = date;
        Description = description;
        DueDate = dueDate;
        Status = status;
        CustomerId = customerId;
        Customer = customer;
        ReferenceNumber = referenceNumber;
        ReferenceDate = referenceDate;
        PaymentMethod = paymentMethod;
    }

    public virtual void AddItem(
        Guid productId,
        Product product,
        decimal quantity,
        decimal unitPrice,
        decimal discountAmount,
        decimal taxAmount)
    {
        var item = InvoiceItem.Create(
            Id,
            this,
            productId,
            product,
            quantity,
            unitPrice,
            discountAmount,
            taxAmount);

        Items.Add(item);
        CalculateTotals();
    }

    public void RemoveItem(Guid itemId)
    {
        var item = Items.FirstOrDefault(i => i.Id == itemId);
        if (item != null)
        {
            Items.Remove(item);
            CalculateTotals();
        }
    }

    protected void CalculateTotals()
    {
        SubTotal = Items.Sum(i => i.TotalAmount);
        TaxAmount = Items.Sum(i => i.TaxAmount);
        DiscountAmount = Items.Sum(i => i.DiscountAmount);
        TotalAmount = SubTotal + TaxAmount - DiscountAmount;
    }
} 