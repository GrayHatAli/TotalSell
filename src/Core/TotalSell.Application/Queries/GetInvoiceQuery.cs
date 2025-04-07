using MediatR;
using TotalSell.Application.Common;
using TotalSell.Application.DTOs;

namespace TotalSell.Application.Queries;

public class GetInvoiceQuery : BaseQuery, IRequest<InvoiceDto>
{
    public required Guid Id { get; set; }
} 