using MediatR;
using TotalSell.Application.DTOs;

namespace TotalSell.Application.Commands;

public class CreateInvoiceCommand : IRequest<Guid>
{
    public required string Number { get; set; }
    public required DateTime Date { get; set; }
    public required Guid CustomerId { get; set; }
    public string? Description { get; set; }
    public string? PaymentTerms { get; set; }
    public required DateTime DueDate { get; set; }
    public required List<InvoiceItemDto> Items { get; set; }
} 