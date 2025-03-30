namespace TotalSell.Application.Commands;

public class CreateInvoiceCommand : BaseCommand
{
    public string Number { get; set; } = null!;
    public DateTime Date { get; set; }
    public string? Description { get; set; }
    public string? PaymentTerms { get; set; }
    public DateTime? DueDate { get; set; }
    public List<CreateInvoiceItemCommand> Items { get; set; } = new();
}

public class CreateInvoiceItemCommand
{
    public Guid ProductId { get; set; }
    public int Quantity { get; set; }
    public decimal UnitPrice { get; set; }
    public decimal DiscountAmount { get; set; }
    public decimal TaxAmount { get; set; }
} 