using MediatR;
using TotalSell.Domain.Enums;

namespace TotalSell.Application.Commands;

public class CreateInvoiceCommand : BaseCommand, IRequest<Guid>
{
    public required string Number { get; set; }
    public required DateTime Date { get; set; }
    public string? Description { get; set; }
    public required DateTime DueDate { get; set; }
    public required InvoiceStatus Status { get; set; }
    public required InvoiceType Type { get; set; }
    public required Guid CustomerId { get; set; }
    public Guid? SupplierId { get; set; }
    public string? ReferenceNumber { get; set; }
    public DateTime? ReferenceDate { get; set; }
    public string? PaymentMethod { get; set; }
    public required List<CreateInvoiceItemCommand> Items { get; set; }
}

public class CreateInvoiceItemCommand
{
    public required Guid ProductId { get; set; }
    public required decimal Quantity { get; set; }
    public required decimal UnitPrice { get; set; }
    public decimal DiscountAmount { get; set; }
    public decimal TaxAmount { get; set; }
}
