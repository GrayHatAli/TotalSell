namespace TotalSell.Domain.Entities;

public abstract class Invoice : BaseEntity
{
    public string Number { get; protected set; }
    public DateTime Date { get; protected set; }
    public string Description { get; protected set; }
    public decimal SubTotal { get; protected set; }
    public decimal TaxAmount { get; protected set; }
    public decimal DiscountAmount { get; protected set; }
    public decimal TotalAmount { get; protected set; }
    public string PaymentTerms { get; protected set; }
    public DateTime? DueDate { get; protected set; }
    public string Status { get; protected set; }
    public ICollection<InvoiceItem> Items { get; protected set; }

    protected Invoice()
    {
        Items = new List<InvoiceItem>();
    }

    protected void CalculateTotals()
    {
        SubTotal = Items.Sum(item => item.TotalAmount);
        TotalAmount = SubTotal + TaxAmount - DiscountAmount;
    }
} 