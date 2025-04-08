using MediatR;
using TotalSell.Application.DTOs;

namespace TotalSell.Application.Queries;

public class GetInvoiceQuery : IRequest<InvoiceDto>
{
    public required Guid Id { get; set; }
} 