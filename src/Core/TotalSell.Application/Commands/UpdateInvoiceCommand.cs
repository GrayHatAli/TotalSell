using MediatR;
using TotalSell.Application.Common;
using TotalSell.Application.DTOs;
using TotalSell.Domain.Enums;

namespace TotalSell.Application.Commands;

public class UpdateInvoiceCommand : BaseCommand, IRequest<Unit>
{
    public new required Guid Id { get; set; }
    public required string Number { get; set; }
    public required DateTime Date { get; set; }
    public required Guid CustomerId { get; set; }
    public string? Description { get; set; }
    public decimal SubTotal { get; set; }
    public decimal TaxAmount { get; set; }
    public decimal DiscountAmount { get; set; }
    public decimal TotalAmount { get; set; }
    public string? PaymentTerms { get; set; }
    public required DateTime DueDate { get; set; }
    public InvoiceStatus Status { get; set; }
    public required List<InvoiceItemDto> Items { get; set; }
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