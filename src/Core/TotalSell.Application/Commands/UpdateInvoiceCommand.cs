namespace TotalSell.Application.Commands;

public class UpdateInvoiceCommand : BaseCommand
{
    public new Guid Id { get; set; }
    public string Number { get; set; } = null!;
    public DateTime Date { get; set; }
    public string? Description { get; set; }
    public string? PaymentTerms { get; set; }
    public DateTime? DueDate { get; set; }
    public string Status { get; set; } = null!;
    public Guid CustomerId { get; set; }
    public IEnumerable<UpdateInvoiceItemCommand> Items { get; set; } = new List<UpdateInvoiceItemCommand>();
}

public class UpdateInvoiceItemCommand
{
    public Guid Id { get; set; }
    public Guid ProductId { get; set; }
    public decimal Quantity { get; set; }
    public decimal UnitPrice { get; set; }
    public decimal DiscountAmount { get; set; }
    public decimal TaxAmount { get; set; }
} 